import yaml

import common_constants
from ExerciseSegment import ExerciseSegment
    
class ExerciseSession:
    
    name = ''
    number_of_segments = 0
    segment_list = []
    file_path = ''


    # sanitise values in exercise programme yaml file, substitute special values and perform calculations                             
    def calc_programme_value(node,read_type):

        if (read_type == 'power'):
            if 'REST' in str(node):
                node = node.replace('REST',str(user_profile['REST']))
            if 'FTP' in str(node):
                node = node.replace('FTP',str(user_profile['FTP']))
            if 'MAP' in str(node):
                node = node.replace('MAP',str(user_profile['MAP']))
            if 'LASTPWR' in str(node):
                node = node.replace('LASTPWR',str(last_power))

        elif (read_type == 'cadence'):
            if 'IDLE' in str(node):
                node = node.replace('IDLE',str(user_profile['IDLE']))
            if 'LOW' in str(node):
                node = node.replace('LOW',str(user_profile['LOW']))
            if 'MED' in str(node):
                node = node.replace('MED',str(user_profile['MED']))
            if 'HIGH' in str(node):
                node = node.replace('HIGH',str(user_profile['HIGH']))
            if 'SPRINT' in str(node):
                node = node.replace('SPRINT',str(user_profile['SPRINT']))
            if 'LASTCAD' in str(node):
                node = node.replace('LASTCAD',str(last_cadence))

        elif (read_type == 'heart'):
            if 'Z2' in str(node):
                node = node.replace('Z2',str(user_profile['Z2']))
            if 'Z3' in str(node):
                node = node.replace('Z3',str(user_profile['Z3']))
            if 'Z4' in str(node):
                node = node.replace('Z4',str(user_profile['Z4']))
            if 'Z5' in str(node):
                node = node.replace('Z5',str(user_profile['Z5']))
            if 'MAX' in str(node):
                node = node.replace('MAX',str(user_profile['MAX']))
            if 'LASTHR' in str(node):
                node = node.replace('LASTHR',str(last_heart))

        elif (read_type == 'description'):
            if len(node) > MAX_DESCRIPTION_LENGTH:
                result = node[:MAX_DESCRIPTION_LENGTH]
                node = result
            clean_node = re.sub("[\s]{2,}",' ',node)
            output = str(clean_node)
        
        if (read_type != 'description'):
            clean_node = re.sub("[^\d\.\*\+\-\/\(\)]+",'',node)
            clean_node = re.sub("[\s]+",'',clean_node)
            output = int(pdeval(clean_node))

        return(output)
# END SANITSE INPUT          



    
    
    def __init__(self, file_path):

        print('Exercise Session loading segments...')
        with open(file_path,'r') as file:
            exercise_programme = yaml.safe_load(file)

        self.name = str(exercise_programme['metadata']['name'])
        self.number_of_segments = len(exercise_programme['segments'])


        i=0
        while i < self.number_of_segments:
            print("\tloading segment " + str(i))
            this_segment = exercise_programme['segments'][i]

            unparsed_target_power = ''
            unparsed_target_cadence = ''
            unparsed_target_heart = ''
            unparsed_target_time = ''
            raw_description = ''
            raw_target = ''
            
            if 'power' in this_segment:
                unparsed_target_power = str(this_segment['power'])

            if 'cadence' in this_segment:
                unparsed_target_cadence =str(this_segment['cadence'])
            
            if 'heart' in this_segment:
                unparsed_target_heart = str(this_segment['heart'])
            
            if 'time' in this_segment:
                unparsed_target_time = str(this_segment['time'])
            else:
                print('Error - Each segment must have a time target. Invalid entry : ' + uparsed_target_time)
                exit()
                
            if 'description' in this_segment:
                raw_description = str(this_segment['description'])

            if 'target' in this_segment:
                raw_target = str(this_segment['target'])

                
            this_segment_object = ExerciseSegment(unparsed_target_power,unparsed_target_cadence,unparsed_target_heart,unparsed_target_time,raw_description,raw_target)

            self.segment_list.append(this_segment_object)
            i=i+1
