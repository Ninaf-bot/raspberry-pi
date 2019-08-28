import threading 
import math
import RPi.GPIO as GPIO
import smbus 
import time
from gpiozero import Robot
from gpiozero import PWMOutputDevice

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
GPIO.setmode(GPIO.BCM)
GPIO.setup(A,GPIO.IN)
GPIO.setup(B,GPIO.IN)
counterA=0
counterB=0
laststateA= GPIO.input(A)

ly=0
lx=0

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

in1=17
in2=27
in3=23
in4=24
en1=PWMOutputDevice(18)
en2=PWMOutputDevice(19)
GPIO.setmode(GPIO.BCM)
robot = Robot((in1, in2), (in3, in4))
speed=1

en1.value=speed
en2.value=speed

#def user_input():
#   while 1: 
#      global speed
#      i=input("Please enter a number: ")
#      print ('wrong input')
#      if i== 'w':
#         robot.forward()
#      elif i=='s':
#         robot.backward()
#      elif i=='a':
#         robot.left()
#      elif i=='d':
#         robot.right()
#      elif i=='x':
#         robot.stop()
#      elif i=='r':
#         speed+=0.1
#      elif i=='f':
#         speed-=0.1
#      else: 
#         print ('wrong input')
#      en1.value=speed

def print_square():
    while 1:
      global lx,ly,counterA,laststateA
      x_out=magneto_read(0x00)
      y_out=magneto_read(0x02)
      z_out=magneto_read(0x04)
      x_out=x_out-x_offset
      y_out=y_out-y_offset
      z_out=z_out-z_offset
      angle=math.atan2(y_out,x_out)+declination
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
      if angle<0:
          angle=angle+2*math.pi
      angle=float(angle)
      angle=float(angle*180/math.pi)
      print ("lx: %d ly: %d angle: %f "%(lx,ly,angle))
      time.sleep(0.01)

      


t1 = threading.Thread(target=print_square) 
#t2 = threading.Thread(target=user_input) 
  
    # starting thread 1 
t1.start() 
    # starting thread 2 
#t2.start() 
while 1: 
      i=input("Please enter a number: ")
      print ('wrong input')
      if i== 'w':
         robot.forward()
      elif i=='s':
         robot.backward()
      elif i=='a':
         robot.left()
      elif i=='d':
         robot.right()
      elif i=='x':
         robot.stop()
      elif i=='r':
         speed+=0.1
      elif i=='f':
         speed-=0.1
      else: 
         print ('wrong input')
      en1.value=speed  
    