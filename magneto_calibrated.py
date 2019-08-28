import smbus
import time
import math
bus = smbus.SMBus(1)
d_address = 0x0d
declination=-0.002327
x_l=0x00
y_l=0x02
z_l=0x04


def magneto_start():
    bus.write_byte_data(d_address,0x09,0x0d)
    bus.write_byte_data(d_address,0x0d,0x01)

def magneto_read(adr):
    low = bus.read_byte_data(d_address, adr)
    high = bus.read_byte_data(d_address, adr+1)
    val=(high<<8)+low
    if(val > 32768):
           val = val - 65536
    return val

magneto_start() 
x_min=y_min=z_min=32767 
x_max=y_max=z_max=-32767 
while 1:
    x=magneto_read(0x00)
    y=magneto_read(0x02)
    z=magneto_read(0x04)
    if x < x_min:
       x_min=x
    if x > x_max:
       x_max=x
    if y < y_min:
       y_min=y
    if y > y_max:
       y_max=y
    if z < z_min:
       z_min=z
    if z > z_max:
       z_max=z
    print 'x_min= %i x_max= %i y_min= %i y_max= %i z_min= %i z_max= %i'%(x_min,x_max,y_min,y_max,z_min,z_max)
    time.sleep(0.01)


