#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Return the RetroRules rule

"""
import argparse
import tarfile
import tempfile
import glob
import os
import sys
import logging

sys.path.insert(0, '/home/')
import rpTool

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Parse reaction rules to user defined diameters')
    parser.add_argument('-rule_type', type=str, default='all', choices=['all', 'forward', 'retro'])
    parser.add_argument('-rules_file', type=str, default='None')
    parser.add_argument('-output', type=str)
    parser.add_argument('-diameters', type=str, default='2,4,6,8,10,12,14,16')
    parser.add_argument('-output_format', type=str, default='csv', choices=['csv', 'tar'])
    params = parser.parse_args()
    try:
        diameters = [int(i) for i in params.diameters.split(',')]
        valid_diameters = []
        for i in diameters:
            if i not in [2,4,6,8,10,12,14,16]:
                logging.warning('Diameters must be either 2,4,6,8,10,12,14,16. Ignoring entry: '+str(i))
            else:
                valid_diameters.append(i)
    except ValueError:
        logging.error('Invalid diamter entry. Must be int of either 2,4,6,8,10,12,14,16')
        exit(1)
    if params.rules_file=='None' or params.rules_file==None:
        rpTool.passRules(params.rule_type, params.output, valid_diameters, params.output_format)
    else:
        rpTool.parseRules(params.rules_file, params.output, valid_diameters, params.output_format)
