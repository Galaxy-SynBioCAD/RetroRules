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

sys.path.insert(0, '/home/')
import rpTool

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to add cofactors to generate rpSBML collection')
    parser.add_argument('-rule_type', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-diameters', type=str)
    parser.add_argument('-output_format', type=str)
    params = parser.parse_args()
    rpTool.passRules(params.rule_type, params.output, [int(i) for i in params.diameters.split(',')], params.output_format)
