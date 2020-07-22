#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Extract the sink from an SBML into RP2 friendly format

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


##
#
#
def main(output, output_format='tar', rule_type='retro', diameters='2,4,6,8,10,12,14,16', rules_file='None', input_format='csv'):
    docker_client = docker.from_env()
    image_str = 'brsynth/retrorules-standalone:v2'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    #create a temporary folder to make the connection between the 
    #docker and the local files
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        if os.path.exists(rules_file):
            shutil.copy(rules_rall, tmpOutputFolder+'/rules.dat')
            command = ['/home/tool_RetroRules.py',
                       '-rule_type',
                       str(rule_type),
                       '-rules_file',
                       '/home/tmp_output/rules.dat',
                       '-diameters',
                       str(diameters),
                       '-output_format',
                       str(output_format),
                       '-input_format',
                       str(input_format),
                       '-output',
                       '/home/tmp_output/output.dat']
        else:
            command = ['/home/tool_RetroRules.py',
                       '-rule_type',
                       str(rule_type),
                       '-rules_file',
                       'None',
                       '-diameters',
                       str(diameters),
                       '-output_format',
                       str(output_format),
                       '-input_format',
                       str(input_format),
                       '-output',
                       '/home/tmp_output/output.dat']
        container = docker_client.containers.run(image_str, 
                                                 command, 
                                                 detach=True,
                                                 stderr=True,
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        err_str = err.decode('utf-8')
        print(err_str)
        if not 'ERROR' in err_str:
            shutil.copy(tmpOutputFolder+'/output.dat', output)
        container.remove()


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to add cofactors to generate rpSBML collection')
    parser.add_argument('-rule_type', type=str, default='all', choices=['all', 'forward', 'retro'])
    parser.add_argument('-rules_file', type=str, default='None')
    parser.add_argument('-output', type=str)
    parser.add_argument('-diameters', type=str, default='2,4,6,8,10,12,14,16')
    parser.add_argument('-output_format', type=str, default='csv', choices=['csv', 'tar'])
    parser.add_argument('-input_format', type=str, default='csv', choices=['csv', 'tsv'])
    params = parser.parse_args()
    main(params.output, params.output_format, params.rule_type, params.diameters, params.rules_file, params.input_format)
