import PySimpleGUI as sg

import time
import sys
import os
import sqlite3

classes_path = os.path.join(os.path.dirname(__file__), 'classes')

#sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'classes'))
#sys.path.append('/Users/martinlee/projects/blue_heart_rate/PARTS3/classes')
sys.path.append(classes_path)

import common_constants
import GuiDisplay
from UserProfile import UserProfile
from ExerciseSession import ExerciseSession
from Biometrics import Biometrics
from FitnessMachine import FitnessMachine


EXERCISE_FILE = os.path.dirname(__file__) + '/exercise_file.yaml'

# INITIALISE GUI
#gui_display = GuiDisplay

# LOAD USER PROFILE
print ('loading user profile')
user_profile  = UserProfile(os.path.dirname(__file__) + common_constants.USER_PROFILE_FILE)

# LOAD EXERCISE PROGRAMME
print ('loading exercise programme')
exercise_programme = ExerciseSession(EXERCISE_FILE)


# INITIALISE VARIABLES
elapsed_time = 0
window = sg.Window('Turbo Workout', GuiDisplay.layout)

biometrics = Biometrics()
fitness_machine = FitnessMachine()

old_i = -1
i=0

print ('beginning workout')
while i < exercise_programme.number_of_segments :
    event, values = window.read(timeout = 10)
    
    if old_i != i:
        this_segment_object = exercise_programme.segment_list[i]

        if i+1 < exercise_programme.number_of_segments :
            next_segment_object = exercise_programme.segment_list[i+1]
        old_i = i
        this_segment_object.start_time = time.time()

        this_segment_object.calculate_targets(fitness_machine.last_power,fitness_machine.last_cadence,biometrics.last_heartrate,user_profile)
                    
        heart_select = power_select = cadence_select = ''
        time_select = '*'
        if str(this_segment_object.target_goal) == 'heart':
            heart_select = '*'
            time_select = ''
        if str(this_segment_object.target_goal) == 'power':
            power_select = '*'
            time_select = ''
        if str(this_segment_object.target_goal) == 'cadence':
            cadence_select = '*'
            time_select = ''


        window['target_cadence_text'].update(str(this_segment_object.cadence_target) + ' ' + cadence_select)
        window['target_power_text'].update(str(this_segment_object.power_target) + ' ' + power_select)            
        window['target_heart_text'].update(str(this_segment_object.heart_target) + ' ' + heart_select)
        window['current_segment_text'].update(str(this_segment_object.description))
        window['next_segment_text'].update(str(next_segment_object.description))    
        print('TARGETS power: ' + str(this_segment_object.power_target) + "\t" + 'cadence: ' + str(this_segment_object.cadence_target) + "\t" + ' heart: ' + str(this_segment_object.heart_target) + "\t" + ' time: ' + str(this_segment_object.time_target))

            
        
        biometrics.pollHeartRate()
        fitness_machine.pollFitnessMachine()

    
    window['current_power_text'].update(str(fitness_machine.current_power) )    
    window['current_cadence_text'].update(str(fitness_machine.current_cadence) )    
    window['current_heart_text'].update(str(biometrics.current_heartrate) )
    window['segment_time_text'].update(str(time_select)+ ' ' +str(elapsed_time) + ' / ' + str(this_segment_object.time_target) )    
    

    print('CURRENT power: ' + str(fitness_machine.current_power) + "\t" + 'cadence: ' + str(fitness_machine.current_cadence) + "\t" + ' heart: ' + str(biometrics.current_heartrate) + "\t" + ' time: ' + str(elapsed_time))
    
    time.sleep(1)
    
    current_time = time.time()
    elapsed_time = int(current_time - this_segment_object.start_time)


# CHECK END OF SEGMENT CONDITION 
    if ( (elapsed_time >= this_segment_object.time_target)
         or (
         (this_segment_object.target_goal == 'power' and fitness_machine.current_power >= this_segment_object.power_target) or
         (this_segment_object.target_goal == 'cadence' and fitness_machine.current_cadence >= this_segment_object.cadence_target) or
         (this_segment_object.target_goal == 'heart' and biometrics.current_heartrate >= this_segment_object.heart_target)
             )
         ):
        old_i = i
        i = i + 1
        print ("NEW SEGMENT")
