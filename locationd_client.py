import smbus 
from time import sleep
import math
import RPi.GPIO as GPIO
import socket


TCP_IP= '192.168.0.104'  # The server's hostname or IP address
TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
laststateA= GPIO.input(A)
ly=0
lx=0


magneto_start()
s.connect((TCP_IP, TCP_PORT))
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
    ls=str(ly)+','+str(lx)
    ls=ls.encode()
    s.send(b'ack1')
    while 1:
        st=s.recv(1024)
        st=st.decode()
        if st== 'ack2':
            s.send(ls)
            break
    while 1:
        st=s.recv(1024)
        st=st.decode()
        if st== 'ack3':
            break
           
    print ("counterA=%f,"%counterA," ly= %f,"%ly,"lx=%f,"%lx,"angle= %f"%angle)
    #sleep(0.1)
s.close()
