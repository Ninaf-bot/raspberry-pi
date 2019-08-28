from gpiozero import Robot
from gpiozero import PWMOutputDevice
import RPi.GPIO as GPIO 

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

while 1:
   input=raw_input()
   if input== 'w':
     robot.forward()
   elif input=='s':
     robot.backward()
   elif input=='a':
     robot.left()
   elif input=='d':
     robot.right()
   elif input=='x':
     robot.stop()
   elif input=='r':
     speed+=0.1
   elif input=='f':
     speed-=0.1
   else: 
     print 'wrong input'
   en1.value=speed