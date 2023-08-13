import os
import sys
import sqlite3

curr_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
import common_constants

class Biometrics:

    current_heartrate = 0
    last_heartrate = 0
    database_connection = ''

    def pollHeartRate(self):

        count = 0
        max_count = 3
        old_heartrate = self.current_heartrate
# three tries to see if we can get heart rate
        while count <= max_count: 
        
            try:
                cursor = self.database_connection.cursor()
                record = cursor.execute('SELECT heart_rate from human_values').fetchall()
                if record:
                    self.current_heartrate=int(record[0][0])
                else:
                    print('Error - no recorded heart rate')
                    self.current_heartrate = 0
            except:
                self.database_connection.close()
                myDB = sqlite3.connect(common_constants.SQLITE_FILE)
                self.database_connection = myDB

            count = count + 1
            if self.current_heartrate > 0:
                break
        self.last_heartrate = old_heartrate
            
    
    def __init__(self):

        myDB = sqlite3.connect(common_constants.SQLITE_FILE)
        self.database_connection = myDB





