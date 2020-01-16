#!/usr/bin/python

'''
HC-SR04 Module
VCC  Connect to (2)
GND  Connect to (6)
TRIG Connect to (11)
ECHO Connect to R1(1K) connect to R2(2K) connect to (2)
                       connect to (12)

             3V3  (1) (2)  5V    
           GPIO2  (3) (4)  5V    
           GPIO3  (5) (6)  GND   
           GPIO4  (7) (8)  GPIO14
             GND  (9) (10) GPIO15
          GPIO17 (11) (12) GPIO18
          GPIO27 (13) (14) GND   
          GPIO22 (15) (16) GPIO23
             3V3 (17) (18) GPIO24
          GPIO10 (19) (20) GND   
           GPIO9 (21) (22) GPIO25
          GPIO11 (23) (24) GPIO8 
             GND (25) (26) GPIO7 
           GPIO0 (27) (28) GPIO1 
           GPIO5 (29) (30) GND   
           GPIO6 (31) (32) GPIO12
          GPIO13 (33) (34) GND   
          GPIO19 (35) (36) GPIO16
          GPIO26 (37) (38) GPIO20
             GND (39) (40) GPIO21

'''
#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD/BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 11
GPIO_ECHO = 12

#set GPIO direction (IN/OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger with a pulse of 0.00001s
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # Wait for the echo and record the time
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime

    # Calculate the distance
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print ("Measurement stopped by user")
        GPIO.cleanup()
