import smbus 
import time 
import math 
bus = smbus.SMBus(1) 
d_address = 0x0d 
declination=-0.002327 
x_l=0x00 
y_l=0x02 
z_l=0x04
x_offset=8944
y_offset=4799
z_offset=5652

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
while 1:
    x_out=magneto_read(0x00)
    y_out=magneto_read(0x02)
    z_out=magneto_read(0x04)
    x_out=x_out-x_offset
    y_out=y_out-y_offset
    z_out=z_out-z_offset
    angle=math.atan2(y_out,x_out)+declination
    angle=float(angle)
    angle=float(angle*180/math.pi)
    if angle<0:
       angle=angle+360
    print ("x: %d y: %d z:%d angle: %f "%(x_out,y_out,z_out,angle))
    time.sleep(0.01)
