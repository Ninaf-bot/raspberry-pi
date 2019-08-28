import smbus
import serial
import time
import math
import string
from gpiozero import robot
from gpiozero import PMWOutputDevice


port='/dev/ttyAMA0'
ser=serial.Serial(port,9600,timeout=0.5)

bus=smbus.SMbus()
declination=-0.002327
x_l=0x00
y_l=0x02
z_l=0x04
def magneto_start():
   bus.write_byte_data(d_address,0x09,0x0d)
   bus.write_byte_data(d_address,0x0b,0x01)

def magneto_read(addr):
   low=bus.read_byte_data(d_address,addr)
   high=bus.read_byte_data(d_address,addr+1)
   value=(high<<8)+low
   return value

def angle_read()
   x_m=magneto_read(x_l)
   y_m=magneto_read(y_l)
   z_m=magneto_read(z_l)
   angle=atan2(y_m,x_m)+declination
   angle=float(angle)
   angle=float(angle*180/math.pi)
   return angle

def gps_read()
   while g==1:
    data_gps = ser.readline()
    if data_gps[0:6]=='$GPGGA':
        try:
           lat=float(data_gps[17:27])
           long=float(data_gps[30:41])
           print("lattitude : %f longitude : %f "%(lat,long))
           return x_resent=
           return y_resent=
           g=0
          
           #have to conver to decimal
        except:
            print('gps data loading')


magneto_start()

x_destination=
y_destination=

while 1:
   gps_read()
   angle_read()
   slope=(y_destination-y_resent)/(x_destination-y_resent)
   if slope<=1
      y=slope*x-slope*x_resent+y_resent
   

