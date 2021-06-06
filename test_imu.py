from nanpy import ArduinoApi, SerialManager, wire
from nanpy.i2c import I2C_Master
import math
from time import sleep as sleep

#L'arduino a une taille limité de données contrairement à python
#donc on limite à 16 bits
def ulong_to_long(u):
    ''' using subtraction '''
    return u - (1<<16) if u >= (1<<15) else u

try:
    connection = SerialManager(device="com3")
    a = ArduinoApi(connection =connection)
    print('connected')
except:
    print('Error: No Arduino found...')

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
   
MPU_address = 0x68   
master = I2C_Master(wire.Wire(connection = connection))  
master.send(MPU_address, [0x6B,0])

while (True):

    master.send(MPU_address, [0x3B])
    data = master.request(MPU_address, 14)

    accX = ulong_to_long(data[0] << 8) | data[1]
    accY = ulong_to_long(data[2] << 8) | data[3]
    accZ = ulong_to_long(data[4] << 8) | data[5]
    
    xAngle = _map(accX, 265, 402, -90, 90)
    yAngle = _map(accY, 265, 402, -90, 90)
    zAngle = _map(accZ, 265, 402, -90, 90)

    #print("x= ", math.degrees(math.atan2(-yAngle, -zAngle) + math.pi))
    #print("y= ", math.degrees(math.atan2(-xAngle, -zAngle) + math.pi))
    print("z= ", math.degrees(math.atan2(-yAngle, -xAngle) + math.pi))
    sleep(0.4)