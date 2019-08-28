import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from drawnow import *
GPIO.setmode(GPIO.BCM)
A=19
B=26
GPIO.setup(A,GPIO.IN)
GPIO.setup(B,GPIO.IN)
counterA=0
counterB=0
distance=[]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
fig.show()
def makeFig():
    
    
    #plt.ylim(80,90)                                 #Set y min and max values
    plt.title('My Live Streaming Sensor Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('distance')                            #Set ylabels
    plt.plot(distance)       #plot the temperature
    #plt.legend(loc='upper left')

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
   distance.append(counterA)
   drawnow(makeFig)
   print (" A= %i B=%i" %(counterA,counterB))
