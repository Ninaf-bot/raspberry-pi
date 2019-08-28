import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
A=19
B=26
GPIO.setup(A,GPIO.IN)
GPIO.setup(B,GPIO.IN)
counterA=0
counterB=0
laststateA= GPIO.input(A)
laststateB= GPIO.input(B)
while 1 :
   stateA=GPIO.input(A)
   stateB=GPIO.input(B)
   if stateA != laststateA :
        counterA=counterA+1
   if stateB !=laststateB :
        counterB=counterB+1
   laststateA=stateA
   laststateB=stateB
   print (" A= %i B=%i" %(counterA,counterB))

