import sys
import os
import logging
import sqlite3
import threading
from openant.easy.node import Node
from openant.easy.channel import Channel
from openant.base.message import Message
from openant.devices import ANTPLUS_NETWORK_KEY

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),''))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'classes'))

import common_constants

HEART_MONITOR_DEVICE_TYPE = int(120)
SCAN_TIME_PERIOD = int(16070)
CHANNEL_RF_FREQ = int(57)
SEARCH_TIMEOUT = int(20)

# setup logging
log = logging.getLogger('HeartRateMeasure')
os.makedirs(os.path.dirname(common_constants.LOGFILE), exist_ok=True)
fh = logging.FileHandler(common_constants.LOGFILE, mode="w", encoding=None, delay=False)
log.addHandler(fh)

# INITIALISE SQLITE DB
try:
    myDB = sqlite3.connect(common_constants.SQLITE_FILE)
    cursor = myDB.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS human_values (heart_rate INTEGER)')
    cursor.execute('delete from human_values')
    myDB.commit()
    myDB.close()
except:
    log.error('Unable to initialise SQLite')
    exit()
    
def on_data(data):
    print("Data Recevied")
    heart_rate = int(data[7])
    log.debug('Received heart rate '+str(heart_rate))
    try:
        myDB = sqlite3.connect(common_constants.SQLITE_FILE)
        cursor = myDB.cursor()
        cursor.execute("update human_values set heart_rate = ?",(heart_rate,))
        myDB.commit()
        myDB.close()
    except:
        log.error('Unable to record heart rate in SQLite')
        
def on_found(data):
    log.info('Found device' + str(data))

    
def back_thread(node):
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)
    channel = node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)

    channel.on_broadcast_data = on_data
    channel.on_burst_data = on_data

    channel.set_period(SCAN_TIME_PERIOD)
    channel.set_search_timeout(SEARCH_TIMEOUT)
    channel.set_rf_freq(CHANNEL_RF_FREQ)
    channel.set_id(0,HEART_MONITOR_DEVICE_TYPE,0)

    try:
        channel.open()
        node.start()

    finally:
        channel.close()
        node.stop()
        print("ANT Shutdown complete")


node = Node()
x = threading.Thread(target=back_thread, args=(node,))
x.start()



