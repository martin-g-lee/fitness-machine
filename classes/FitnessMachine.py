import os
import sys
import sqlite3

curr_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
import common_constants

class FitnessMachine:

    current_power = 0
    current_cadence = 0
    last_power = 0
    last_cadence = 0
    database_connection = ''

    def pollFitnessMachine(self):

        count = 0
        max_count = 3
        old_power = self.current_power
        old_cadence = self.current_cadence
        
# three tries to see if we can get power & cadence
        while count <= max_count: 
        
            try:
                cursor = self.database_connection.cursor()
                record = cursor.execute('SELECT power,cadence from bike_values').fetchall()
                if record:
                    self.current_power=int(record[0][0])
                    self.current_cadence=int(record[0][1])
                else:
                    print('Error - no fitness machine data')
                    self.current_power = 0
                    self.current_cadence = 0
            except:
                self.database_connection.close()
                myDB = sqlite3.connect(common_constants.SQLITE_FILE)
                self.database_connection = myDB

            count = count + 1
            if self.current_power > 0 or self.current_cadence > 0:
                break
            
        self.last_power = old_power
        self.last_cadence = old_cadence
            
    
    def __init__(self):

        myDB = sqlite3.connect(common_constants.SQLITE_FILE)
        self.database_connection = myDB





