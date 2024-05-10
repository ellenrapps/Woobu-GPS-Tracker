'''
Credits to ahmadlogs: https://github.com/ahmadlogs/rpi-pico-upy/blob/main/gps-rpi-pico/gps-rpi-pico.py
'''

import machine
from machine import Pin, UART
import utime, time


#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

#print gps module connection details
print(gps_module)

#Used to Store NMEA Sentences
buff = bytearray(255)

TIMEOUT = False

#store the status of satellite is fixed or not
FIX_STATUS = False

#Store GPS Coordinates
latitude = ""
longitude = ""
satellites = ""
gpsTime = ""


#function to get gps Coordinates
def getPositionData(gps_module):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, gpsTime
    
    #run while loop to get gps data
    timeout = time.time() + 8   # 8 seconds from now
    while True:
        gps_module.readline()
        buff = str(gps_module.readline())
        #parse $GPGGA term
        #b'$GPGGA,094840.000,2941.8543,N,07232.5745,E,1,09,0.9,102.1,M,0.0,M,,*6C\r\n'
        #print(buff)
        parts = buff.split(',')
        
        #if no gps displayed remove "and len(parts) == 15" from below if condition
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                #UTC time is parts[1]
                #Latitude is parts[2]
                #N/S is parts[3]
                #Longitude is parts[4]
                #E/W is parts[5]
                #Position Fix is [6]
                #No. of satellites is parts[7]
                
                latitude = convertToDigree(parts[2])
                # parts[3] contain 'N' or 'S'
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDigree(parts[4])
                # parts[5] contain 'E' or 'W'
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                gpsTime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(100)
        
#function to convert raw Latitude and Longitude
#to actual Latitude and Longitude
def convertToDigree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) #degrees
    nexttwodigits = RawAsFloat - float(firstdigits*100) #minutes
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) # to 6 decimal places
    return str(Converted)
    
    
def la_lo_time_sat():
    global FIX_STATUS, TIMEOUT, latitude, longitude
    while True:
        getPositionData(gps_module)        

        if(FIX_STATUS == True):
            result = (latitude, longitude, gpsTime, satellites)
            return(result)
