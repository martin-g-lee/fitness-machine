import sys
import os
import logging
import sqlite3
import asyncio
from bleak import BleakClient

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),''))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'classes'))

import common_constants


SERVICE_UUID = '00001826-0000-1000-8000-00805f9b34fb' # fitness machine
GATT_UUID = '00002ad2-0000-1000-8000-00805f9b34fb' # indoor bike

# setup logging                                                                                  
log = logging.getLogger('FitnessMachineMeasure')
os.makedirs(os.path.dirname(common_constants.LOGFILE), exist_ok=True)
fh = logging.FileHandler(common_constants.LOGFILE, mode="w", encoding=None, delay=False)
log.addHandler(fh)


try:
  myDB = sqlite3.connect(common_constants.SQLITE_FILE)
  cursor = myDB.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS bike_values (power INTEGER, cadence INTEGER)')
  cursor.execute('delete from bike_values')
  myDB.commit()
  myDB.close()
except:
  log.error('Unable to initialise SQLite')
  exit()
  
  
def data_callback(handle, data):
  print(handle, data)

  current_speed = 0
  current_cadence = 0
  current_power = 0

  
  offset = 2  
  current_speed = int.from_bytes(data[offset : offset + 2], "little", signed=False)/100

  offset = 4  
  current_cadence = int.from_bytes(data[offset : offset + 2], "little", signed=False) / 2

  offset = 6
  current_power = int.from_bytes(data[offset : offset + 2], "little", signed=True)

  log.debug('Received bike data. Cadence : ' + str(current_cadence) + "\t" + 'Power : ' + str(current_power) )
  try:
    myDB = sqlite3.connect(common_constants.SQLITE_FILE)
    cursor = myDB.cursor()
    cursor.execute("update bike_values set power = ?, cadence = ?",(current_power,current_cadence))
    myDB.commit()
    myDB.close()
  except:
    log.error('Unable to bike data in SQLite')
    exit()


  
async def main(address):
  async with BleakClient(address) as client:
    if (not client.is_connected):
      log.error('BLE client not connected')
      raise "client not connected"

    try:
      await client.start_notify(GATT_UUID, data_callback)
    except KeyboardInterrupt:
      log.debug('KeyboardInterrupt')
      await client.stop_notify(GATT_UUID)
      exit()
      
if __name__ == "__main__":

  asyncio.run(main(common_constants.MAC_ADDRESS))
