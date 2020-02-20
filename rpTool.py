import shutil
import logging
import csv

def passRules(rule_type, output, diameters):
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
    #### filter the rules by the diameters
    with open(rule_file, 'r') as rf:
        with open(output, 'w') as o:
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
    return True
