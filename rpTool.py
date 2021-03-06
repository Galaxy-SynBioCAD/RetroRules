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


## Parse the input file and return the reactions rules at the appropriate diameters
#
#
def passRules(output, rule_type='all', diameters=[2,4,6,8,10,12,14,16], output_format='csv'):
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
                o_csv = csv.writer(o, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                o_csv.writerow(next(rf_csv))
                for row in rf_csv:
                    try:
                        if int(row[4]) in diameters:
                            o_csv.writerow(row)
                    except ValueError:
                        logging.error('Cannot convert diameter to integer: '+str(row[4]))
                        return False
        if output_format=='tar':
            with tarfile.open(output, mode='w:gz') as ot:
                info = tarfile.TarInfo('Rules.csv')
                info.size = os.path.getsize(outfile_path)
                ot.addfile(tarinfo=info, fileobj=open(outfile_path, 'rb'))
        elif output_format=='csv':
            shutil.copy(outfile_path, output)
        else:
            logging.error('Cannot detect the output_format: '+str(output_format))
            return False
    return True


## Parse the rules if a user inputs it as a file
#
#
def parseRules(rule_file, output, rule_type='all', diameters=[2,4,6,8,10,12,14,16], input_format='csv', output_format='csv'):
    ##### create temp file to write ####
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        ##### parse the input ######
        outfile_path = tmpOutputFolder+'/tmp_rules.csv'
        if input_format=='tsv':
            with open(rule_file, 'r') as in_f:
                with open(outfile_path, 'w') as out_f:
                    out_csv = csv.writer(out_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                    out_csv.writerow([
                        "Rule ID",
                        "Rule",
                        "EC number",
                        "Reaction order",
                        "Diameter",
                        "Score",
                        "Legacy ID",
                        "Reaction direction",
                        "Rule relative direction",
                        "Rule usage",
                        "Score normalized"])
                    for row in csv.DictReader(in_f, delimiter='\t'):
                        try:
                            if int(row['Diameter']) in diameters:
                                if rule_type=='all' or (rule_type=='retro' and (row['Rule_usage']=='both' or row['Rule_usage']=='retro')) or (rule_type=='forward' and (row['Rule_usage']=='both' or row['Rule_usage']=='forward')):
                                    out_csv.writerow([
                                        row['# Rule_ID'],
                                        row['Rule_SMARTS'],
                                        row['Reaction_EC_number'],
                                        row['Rule_order'],
                                        row['Diameter'],
                                        row['Score'],
                                        row['Legacy_ID'],
                                        row['Reaction_direction'],
                                        row['Rule_relative_direction'],
                                        row['Rule_usage'],
                                        row['Score_normalized']])
                        except ValueError:
                            #TODO: consider changing this to warning and passing to the next row
                            logging.error('Cannot convert diameter to integer: '+str(row['Diameter']))
                            return False
        elif input_format=='csv':
            with open(rule_file, 'r') as rf:
                with open(outfile_path, 'w') as o:
                    rf_csv = csv.reader(rf)
                    o_csv = csv.writer(o, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                    o_csv.writerow(next(rf_csv))
                    for row in rf_csv:
                        try:
                            if int(row[4]) in diameters:
                                if rule_type=='all' or (rule_type=='retro' and (row[9]=='both' or row[9]=='retro')) or (rule_type=='forward' and (row[9]=='both' or row[9]=='forward')):
                                    o_csv.writerow(row)
                        except ValueError:
                            logging.error('Cannot convert diameter to integer: '+str(row[4]))
                            return False
        else:
            logging.error('Can only have input formats of TSV or CSV')
            return False
        ##### build the output #####
        if output_format=='tar':
            with tarfile.open(output, mode='w:gz') as ot:
                info = tarfile.TarInfo('Rules.csv')
                info.size = os.path.getsize(outfile_path)
                ot.addfile(tarinfo=info, fileobj=open(outfile_path, 'rb'))
        elif output_format=='csv':
            shutil.copy(outfile_path, output)
        else:
            logging.error('Cannot detect the output_format: '+str(output_format))
            return False
    return True
