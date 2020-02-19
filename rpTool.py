import shutil
import logging

def passRules(rule_type, output):
    if rule_type=='all':
        shutil.copy('/home/rules_rall_rp2.csv', output)
    elif rule_type=='forward':
        shutil.copy('/home/rules_rall_rp2_forward.csv', output)
    elif rule_type=='retro':
        shutil.copy('/home/rules_rall_rp2_retro.csv', output)
    else:
        logging.error('Cannot detect input: '+str(rule_type))
        return False
    return True
