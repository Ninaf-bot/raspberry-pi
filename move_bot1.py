from gpiozero import Robot
from gpiozero import PWMOutputDevice
import RPi.GPIO as GPIO 

in1=17
in2=27
in3=23
in4=24
en1=PWMOutputDevice(18)
GPIO.setmode(GPIO.BCM)
robot = Robot((in1, in2), (in3, in4))

speed=0.6

en1.value=speed

while 1:
   i=input()
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

