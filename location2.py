import smbus 
import time 
import math
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from drawnow import *
bus = smbus.SMBus(1) 
d_address = 0x0d 
declination=-0.002327 
x_l=0x00 
y_l=0x02 
#z_l=0x04
x_offset=8944
y_offset=4799
#z_offset=5652

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
GPIO.setmode(GPIO.BCM)
A=19
B=26
GPIO.setup(A,GPIO.IN)
GPIO.setup(B,GPIO.IN)
counterA=0
#counterB=0
locationy=[]
locationx=[]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
fig.show()
def makeFig():
    
    
    #plt.ylim(80,90)                                 #Set y min and max values
    plt.title('My Live Streaming Sensor Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('distance')                            #Set ylabels
    plt.plot(locationy,locationx)       #plot the temperature
    #plt.legend(loc='upper left')

laststateA= GPIO.input(A)
ly=0
lx=0


magneto_start()
while 1:
    x_out=magneto_read(0x00)
    y_out=magneto_read(0x02)
    z_out=magneto_read(0x04)
    x_out=x_out-x_offset
    y_out=y_out-y_offset
    #z_out=z_out-z_offset
    angle=math.atan2(y_out,x_out)+declination
    #angle=float(angle)
    #angle=float(angle*180/math.pi)
    if angle<0:
       angle=angle+2*math.pi
    stateA=GPIO.input(A)
    stateB=GPIO.input(B)
    if stateA != laststateA :
        counterA=counterA+1
        temp=1
    else :
       temp=0
    laststateA=stateA
    tempy=temp*math.sin(angle)
    tempx=temp*math.cos(angle)
    ly=ly+tempy
    lx=lx+tempx
    locationy.append(ly)
    locationx.append(lx)
    angle=float(angle)
    angle=float(angle*180/math.pi)
    drawnow(makeFig)
    print ("counterA=%f"%counterA," ly= %f "%ly,"lx=%f "%lx,"angle= %f"%angle)
    
