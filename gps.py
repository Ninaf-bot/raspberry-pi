import time
import serial
import string
import math

port = "/dev/ttyAMA0" # the serial port to which the pi is connected.
r=6378137  #radius of the earth in m 
#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
 
while 1:
    data = ser.readline() 
    if data[0:6]=='$GPGGA':
        data=data.split(',')
        lat=data[2]
        lat = float(lat[0:2])+float(lat[2:])/60
        if data[3]=='S':
           lata=-lat
        long=data[4]
        long = float(long[0:3])+float(long[3:])/60
        if data[5]=='W':
           long=-long
        print'lat= %f degrees long = %f degrees'%(lat,long)
        lat=lat*math.pi*r/180
        long=long*math.pi*r/180
        print("lattitude : %f m longitude : %f m "%(lat,long))
    time.sleep(0.05)
