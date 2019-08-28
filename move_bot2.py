from gpiozero import Robot
from gpiozero import PWMOutputDevice
import RPi.GPIO as GPIO
import smbus 
import time 
import math
import socket
import threading

in1=17
in2=27
in3=23
in4=24
en1=PWMOutputDevice(18)
en2=PWMOutputDevice(19)
GPIO.setmode(GPIO.BCM)
robot = Robot((in1, in2), (in3, in4))

speed=0.6

en1.value=speed
en2.value=speed

bus = smbus.SMBus(1) 
d_address = 0x0d 
declination=-0.002327 
x_l=0x00 
y_l=0x02 
z_l=0x04
x_offset=8944
y_offset=4799
z_offset=5652

A=19
B=26
GPIO.setup(A,GPIO.IN)
GPIO.setup(B,GPIO.IN)
counterA=0
counterB=0
laststateA= GPIO.input(A)

ly=0
lx=0
ls=str(ly)+','+str(lx)

TCP_IP= '192.168.0.104'  # The server's hostname or IP address
TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#def send_data():
#    global ls,ly,lx
#    while 1:
#      ls=str(ly)+','+str(lx)
#      ls=ls.encode()
#      s.send(b'ack1')
#      while 1:
#         st=s.recv(1024)
#         st=st.decode()
#         if st== 'ack2':
#             s.send(ls)
#             break
#      while 1:
#         st=s.recv(1024)
#         st=st.decode()
#         if st== 'ack3':
#             break
#           
#     print (" ly= %f,"%ly,"lx=%f,"%lx,"angle= %f"%angle)


def tracking():
  while 1:
    global ly,lx,ls,laststateA,counterA
    x_out=magneto_read(0x00)
    y_out=magneto_read(0x02)
    z_out=magneto_read(0x04)
    x_out=x_out-x_offset
    y_out=y_out-y_offset
    z_out=z_out-z_offset
    angle=math.atan2(y_out,x_out)+declination
    #angle=float(angle)
    #angle=float(angle*180/math.pi)
    if angle<0:
       angle=angle+2*math.pi
    stateA=GPIO.input(A)
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
    #locationy.append(ly)
    #locationx.append(lx)
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
    print (" ly= %f,"%ly,"lx=%f,"%lx,"angle= %f"%angle)                     
    
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
#s.connect((TCP_IP, TCP_PORT))



t2 = threading.Thread(target=tracking)
t2.start()
while 1: 
      i=input()
      print ('wrong input')
      if i== 'w':
         robot.forward()
      elif i=='s':
         robot.backward()
      elif i=='a':
         robot.right()
      elif i=='d':
         robot.left()
      elif i=='x':
         robot.stop()
      elif i=='r':
         speed+=0.1
      elif i=='f':
         speed-=0.1
      else: 
         print ('wrong input')
      en1.value=speed  
   