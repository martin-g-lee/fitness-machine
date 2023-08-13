import os
import sys
import re
from pandas import eval as pdeval


curr_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
import common_constants

class ExerciseSegment:

    description = ''
    target_goal = ''    
    power_target = 0
    cadence_target = 0
    heart_target = 0
    time_target = 0
    unparsed_power_target = ''
    unparsed_cadence_target = ''
    unparsed_heart_target = ''
    unparsed_time_target = ''
    
    def calculate_targets(self,last_power,last_cadence,last_heart,user_profile):

        if self.unparsed_power_target != '':
            temp_value = self.unparsed_power_target
            if 'REST' in str(self.unparsed_power_target):
                temp_value = temp_value.replace('REST',str(user_profile.REST))
            if 'FTP' in self.unparsed_power_target:
                temp_value = temp_value.replace('FTP',str(user_profile.FTP))
            if 'MAP' in self.unparsed_power_target:
                temp_value = temp_value.replace('MAP',str(user_profile.MAP))
            if 'LASTPWR' in self.unparsed_power_target:
                temp_value = temp_value.replace('LASTPWR',str(last_power))
            clean_temp_value = re.sub("\s+",'',temp_value)
            clean_temp_value = re.sub("[^\d\.\*\+\-\/\(\)]+",'',clean_temp_value)
            if clean_temp_value.isdigit():
                self.power_target = int(clean_temp_value)
            else:
                output = int(pdeval(clean_temp_value))
                self.power_target = int(output)
        else:
            self.power_target = 0
                
        if self.unparsed_cadence_target != '':
            temp_value = self.unparsed_cadence_target
            if 'IDLE' in self.unparsed_cadence_target:
                temp_value = temp_value.replace('IDLE',str(user_profile.IDLE))
            if 'LOW' in self.unparsed_cadence_target:
                temp_value = temp_value.replace('LOW',str(user_profile.LOW))
            if 'MED' in self.unparsed_cadence_target:
                temp_value = temp_value.replace('MED',str(user_profile.MED))
            if 'HIGH' in self.unparsed_cadence_target:
                temp_value = temp_value.replace('HIGH',str(user_profile.HIGH))
            if 'SPRINT' in self.unparsed_cadence_target:
                temp_value = temp_value.replace('SPRINT',str(user_profile.SPRINT))
            if 'LASTCAD' in self.unparsed_cadence_target:
                temp_value = temp_value.replace('LASTCAD',str(last_cadence))
            clean_temp_value = re.sub("\s+",'',temp_value)
            clean_temp_value = re.sub("[^\d\.\*\+\-\/\(\)]+",'',clean_temp_value)
            if clean_temp_value.isdigit():
                self.cadence_target = int(clean_temp_value)
            else:
                output = int(pdeval(clean_temp_value))
                self.cadence_target = int(output)
        else:
            self.cadence_taget = 0
                

        if self.unparsed_heart_target != '':
            temp_value = self.unparsed_heart_target
            if 'Z2' in self.unparsed_heart_target:
                temp_value = temp_value.replace('Z2',str(user_profile.Z2))
            if 'Z3' in self.unparsed_heart_target:
                temp_value = temp_value.replace('Z3',str(user_profile.Z3))
            if 'Z4' in self.unparsed_heart_target:
                temp_value = temp_value.replace('Z4',str(user_profile.Z4))
            if 'Z5' in self.unparsed_heart_target:
                temp_value = temp_value.replace('Z5',str(user_profile.Z5))
            if 'MAX' in self.unparsed_heart_target:
                temp_value = temp_value.replace('MAX',str(user_profile.MAX))
            if 'LASTHR' in self.unparsed_heart_target:
                temp_value = temp_value.replace('LASTHR',str(last_heart))
            clean_temp_value = re.sub("\s+",'',temp_value)
            clean_temp_value = re.sub("[^\d\.\*\+\-\/\(\)]+",'',clean_temp_value)
            if clean_temp_value.isdigit():
                self.heart_target = int(clean_temp_value)
            else:
                output = int(pdeval(clean_temp_value))
                self.heart_target = int(output)
        else:
            self.heart_target = 0
        
    
    def __init__(self, unparsed_target_power,unparsed_target_cadence,unparsed_target_heart,unparsed_target_time,raw_description,raw_target):

        self.unparsed_power_target = unparsed_target_power
        self.unparsed_cadence_target = unparsed_target_cadence
        self.unparsed_heart_target = unparsed_target_heart
        self.unparsed_time_target = unparsed_target_time

        if len(raw_description) > common_constants.MAX_DESCRIPTION_LENGTH:
            raw_description = raw_description[:common_constants.MAX_DESCRIPTION_LENGTH]
        raw_description = re.sub("\s{2,}",' ',raw_description)
        self.description = str(raw_description)

        print ('raw : '+str(raw_target))
        self.target_goal = 'time'
        if raw_target == 'heart' or raw_target == 'power' or raw_target == 'cadence':
            self.target_goal = str(raw_target)
        print ('goal : '+str(self.target_goal))
            
        temp_value = self.unparsed_time_target
        temp_value = re.sub("\D+",'',temp_value)
        if temp_value.isdigit():
            self.time_target = int(temp_value)
        else:
            print ('ERROR - each segment must specifiy a time value')
            self.time_target = 30
