import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

in1=
in2=
in3=
in4=
en1=
en2=

GPIO.setup(in1,GPIO.out)
GPIO.setup(in2,GPIO.out)
GPIO.setup(in3,GPIO.out)
GPIO.setup(in4,GPIO.out)
GPIO.setup(en1,GPIO.out)
GPIO.setup(en2,GPIO.out)

def PWM(pin):
      GPIO.output(pin,False)
      time.sleep(0.000005)
      GPIO.output(pin,True)
      time.sleep(0.000005)



def forward():
   
   GPIO.output(in1,False)
   PWM(in2)
   GPIO.output(in3,False)
   PWM(in4)

def backward():
   PWM(in1)
   GPIO.output(in2,False)
   PWM(in3)
   GPIO.output(in4,False)

def right():
   GPIO.output(in1,False)
   PWM(in2)
   GPIO.output(in3,False)
   GPIO.output(in4,False)

def left():
   GPIO.output(in1,False)
   GPIO.output(in2,False)
   GPIO.output(in3,False)
   PWM(in4)
def stop():
   GPIO.output(in1,False)
   GPIO.output(in2,False)
   GPIO.output(in3,False)
   GPIO.output(in4,False)


while 1:
   input=raw_input()
   if input=='w': 
      forward()
   elif input=='s':
     backward()
   elif input=='a':
     left()
   elif input=='d':
     right()
   elif input=='x':
     stop()




