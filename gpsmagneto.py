import time
import smbus 
import math 
import serial
import string

bus = smbus.SMBus(1) 
d_address = 0x0d 
declination=-0.002327 
x_l=0x00 
y_l=0x02 
z_l=0x04

port = "/dev/ttyAMA0" # the serial port to which the pi is connected.

def magneto_start():
    bus.write_byte_data(d_address,0x09,0x0d)
    bus.write_byte_data(d_address,0x0d,0x01)

def magneto_read(adr): 
    low = bus.read_byte_data(d_address, adr) 
    high = bus.read_byte_data(d_address, adr+1)
    val=(high<<8)+low
    return val

magneto_start()

ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

while 1:
    try:
        data_gps = ser.readline()
    except:
        print("loading")
    x_out=magneto_read(0x00)
    y_out=magneto_read(0x02)
    z_out=magneto_read(0x04)
    if data_gps[0:6]=='$GPGGA':
        try:
           lat=float(data_gps[17:27])
           long=float(data_gps[30:41])
           print("lattitude : %f longitude : %f "%(lat,long))
        except:
            print('gps data loading')
    angle=math.atan2(y_out,x_out)+declination
    angle=float(angle)
    angle=int(angle*180/math.pi)

    print "x: %d  y: %d z:%d angle: %f "%(x_out,y_out,z_out,angle)
    time.sleep(0.5)


