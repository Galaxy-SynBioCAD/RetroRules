#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Extract the reaction rules from input reactions or RetroRules file

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


def main(output, output_format='tar', rule_type='retro', diameters='2,4,6,8,10,12,14,16', rules_file='None', input_format='csv'):
    """Parse the rules if a user inputs it as a file

    :param output: Path to the output file
    :param output_format: Format to the output
    :param rule_type: The rule type to return. Valid options: all, forward, retro. (Default: all)
    :param diameters: The diameters to return. Valid options: 2,4,6,8,10,12,14,16. (Default: '2,4,6,8,10,12,14,16')
    :param rules_file: The input rules file (Default: None)
    :param intput_format: The input file format. Valid options: csv, tar. (Default: csv)

    :type output: str 
    :type output_format: str 
    :type rule_type: str
    :type diameters: list
    :type rules_file: str
    :type input_format: str

    :rtype: None
    :return: None
    """
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
        if 'ERROR' in err_str:
            print(err_str)
        elif 'WARNING' in err_str:
            print(err_str)
        if not os.path.exists(tmpOutputFolder+'/output.dat'):
            print('ERROR: Cannot find the output file: '+str(tmpOutputFolder+'/output.dat'))
        else:
            shutil.copy(tmpOutputFolder+'/output.dat', output)
        container.remove()


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
