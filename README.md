# fitness-machine
Turbo trainer workouts via ANT+ and BLE connection to bike trainer in Python.

Project (c) M LEE, made available for use under MIT Licence


GOAL

Sufferfest was no longer offering me what I wanted from my turbo trainer bike. I wanted to create my own fitness workouts which I could synchronise to videos (such as the Workout with GTN videos). Plus I wanted the workouts to be tailored to my power and heart rate ranges.


GET STARTED

Edit the user_profile.yaml file to match your prefered personal statistics

Edit the exercise_file.yaml to create your own workout. Instead of absolute number values for the power, cadence & heart rate targets you can use the mnemonics from your user_profile e.g. FTP, MAP, SPRINT, Z4 etc. You can also define macros to manipulate the mneomonics e.g. 0.9*MAP for 90% of MAP, or FTP-20 for 20W less than your FTP.

The 'target' defines how the segment within the workout will end. If target = 'time', then once the segment has lasted to prescribed time, the segment will end. If target = 'power', then once the power target has been reached, the segment will end.

LASTHR, LASTPWR, LASTCAD mnemonics refer to the last recorded values for heart rate, power & cadence respectively. Hence you can define a segment to reach a specific power and follow that with a segment that maintains the subject at the same heart rate as the previous segment, but with fluctuating power.

Open a new terminal session, enter: python3 services/measure_heart_rate.py  - this will connect to heart rate monitor and record latest value in SQLite DB.

Open another new terminal session, enter: python3 services/measure_fitness_machine.py - this will connect to the turbo trainer and record latest power and cadence values in SQLite DB.
(you will need to edit services/measure_fitness_machine.py to match your device's service and GATT UUIDs. 

You'll also need to edit common_constants.py to include your device's MAC address.)

Open yet another new terminal session, enter: python3 run.py - this will load the workout defined in exercise_file.yaml and create a rudimentary GUI.


PLATFORM

Code developed on MacOS Monterey 12.6.8, with Python 3.11.4. Tested on Wahoo Kickr Core turbo trainer bike.

Uses Bluetooth BLE to connect to trainer, and ANT+ for heart monitor. 


REQUIREMENTS

PySimpleGUI, sqlite3, logging, BleakClient, openant, pandas, yaml


TO DO

Set trainer resistance (not implemented yet)

Proper logging (partially implemented)

Specify exercise.yaml file as command line argument

Rearrange GUI to not look as bad

Record and implement max power / max cadence limits

Write more & better exercise workouts

Multimedia feature, synchronise workout to video, display video alongside GUI


CAUTION

No warranties, use as own risk. Executing this program might break or permanently damage your fitness equipment. Exercise may be detrimental to your health. Intense exercise may be intensely detrimental to your health. You should consult a physician or health professional before you begin an exercise regime and during your regime too. 

If you don't know what MAP, FTP, or Z4 / threshold refers to, then this project is not for you. If you do, hopefully you'll be able to make good use of it.
