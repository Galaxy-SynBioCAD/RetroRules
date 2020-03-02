#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Return RetroRules

"""

import shutil
import logging
import csv
import io
import os
import shutil
import tarfile
import tempfile

def passRules(rule_type, output, diameters, output_format='csv'):
    rule_file = None
    if rule_type=='all':
        rule_file = '/home/rules_rall_rp2.csv' 
    elif rule_type=='forward':
        rule_file = '/home/rules_rall_rp2_forward.csv'
    elif rule_type=='retro':
        rule_file = '/home/rules_rall_rp2_retro.csv'
    else:
        logging.error('Cannot detect input: '+str(rule_type))
        return False
    ##### create temp file to write ####
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        outfile_path = tmpOutputFolder+'/tmp_rules.csv'
        with open(rule_file, 'r') as rf:
            with open(outfile_path, 'w') as o:
                rf_csv = csv.reader(rf)
                o_csv = csv.writer(o, delimiter=',', quotechar='"')
                o_csv.writerow(next(rf_csv))
                for row in rf_csv:
                    try:
                        if int(row[4]) in diameters:
                            o_csv.writerow(row)
                    except ValueError:
                        logging.error('Cannot convert diameter to integer: '+str(row[4]))
                        return False
        if output_format=='csv':
            with tarfile.open(output, mode='w:xz') as ot:
                info = tarfile.TarInfo('Rules.csv')
                info.size = os.path.getsize(outfile_path)
                ot.addfile(tarinfo=info, fileobj=open(outfile_path, 'rb'))
        elif output_format=='tar':
            shutil.copy(outfile_path, output)
        else:
            logging.error('Cannot detect the output_format: '+str(output_format))
            return False
    return True

