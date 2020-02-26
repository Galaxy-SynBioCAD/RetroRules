#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Return the RetroRules rule

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker

def main(rule_type, diameters, output):
    docker_client = docker.from_env()
    image_str = 'brsynth/retrorules-standalone:dev'
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
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        command = ['/home/tool_RetroRules.py',
                   '-rule_type',
                   rule_type,
                   '-diameters',
                   diameters,
                   '-output',
                   '/home/tmp_output/output.dat']
        docker_client.containers.run(image_str, 
                command, 
                auto_remove=True, 
                detach=False, 
                volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        shutil.copy(tmpOutputFolder+'/output.dat', os.getcwd()+'/'+output)

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Return reaction rules in the CSV format')
    parser.add_argument('-rule_type', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-diameters', type=str)
    params = parser.parse_args()
    main(params.rule_type, params.diameters, params.output)
