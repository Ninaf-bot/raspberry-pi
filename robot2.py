import time
import RPi.GPIO as GPIO
import serial
import smbus
from gpiozero import Robot
from gpiozero import PWMOutputDevice
import math
A_encoder=19
GPIO.setup(A_encoder,GPIO.IN)
x_offset=6891
y_offset=732

magneto_address=0x0d
declination=-0.002327 
x_l=0x00
y_l=0x02
#z_l=0x04
in1=17
in2=27
in3=23
in4=24
en1=PWMOutputDevice(18)
en2=PWMOutputDevice(19)

robot = Robot((in1, in2), (in3, in4))
speed=1

en1.value=speed
en2.value=speed

ser=serial.Serial("/dev/ttyAMA0",9600)
bus=smbus.SMBus(1)


def magneto_start():
    bus.write_byte_data(magneto_address,0x09,0x0d)
    bus.write_byte_data(magneto_address,0x0d,0x01)

def magneto_read(adr): 
    low = bus.read_byte_data(magneto_address, adr) 
    high = bus.read_byte_data(magneto_address, adr+1)
    val=(high<<8)+low
    if(val > 32767):
           val = val - 65536
    return val

def angle_read():
    x_out=magneto_read(0x00)
    y_out=magneto_read(0x02)
    #z_out=magneto_read(0x04)
    x_out=x_out-x_offset
    y_out=y_out-y_offset
    angle=math.atan2(y_out,x_out)+declination
    angle=int(angle*180/math.pi)
    if angle<0:
      angle=angle+360
    return angle

def measure_distance_travelled():
    total_pulses=0
    counterA=0
    laststateA= GPIO.input(A_encoder)
    while counterA<200 :
       stateA=GPIO.input(A_encoder)
       if stateA != laststateA :
           counterA=counterA+1
       laststateA=stateA
    total_pulses=total_pulses+counterA
    distance_travelled=total_pulses*0.07695
    return distance_travelled


magneto_start()

while 1:
   
   x_destination=raw_input("enter x co-ordinate of the destination=") 
   y_destination=raw_input("enter y co-ordinate of the destination=")
   x_destination=float(x_destination)
   y_destination=float(y_destination) 
   d_x2=math.pow(x_destination,2.0)
   d_y2=math.pow(y_destination,2.0)
   d=d_x2+d_y2
   d=float(d)   
   distance_to_be_travelled=math.pow(d,0.5)
   angle_desired=math.atan2(y_destination,x_destination)
   angle_desired=int(angle_desired*180/math.pi)
   print angle_desired
   distance_travelled=0
   while distance_travelled < distance_to_be_travelled :
      current_angle=angle_read()
      if current_angle < angle_desired :
           while current_angle < angle_desired :
             
             current_angle=angle_read()

      else if current_angle > angle_desired :
           while current_angle > angle_desired :
             robot.right()
             current_angle=angle_read()
      robot.forward()
      distance_travelled=measure_distance_travelled()
      robot.stop()