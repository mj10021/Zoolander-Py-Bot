# python imports

import sys
from ctypes import *
import time
from time import sleep


# Phidget imports

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, PositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes


# get servo index argument

servo_index = 0

if len(sys.argv) > 1 and int(sys.argv[1]) in range(8) : servo_index = int(sys.argv[1]);

print("starting servo index is %s\n" % str(servo_index))




# create advancedServo object

try:
    advancedServo = AdvancedServo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)


# stack to keep current values in

currentList = [0,0,0,0,0,0,0,0]
velocityList = [0,0,0,0,0,0,0,0]


# display information


def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (advancedServo.isAttached(), advancedServo.getDeviceName(), advancedServo.getSerialNum(), advancedServo.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of motors: %i" % (advancedServo.getMotorCount()))


# event handler callback functions


def Attached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))


def Detached(e):
    detached = e.device
    print("Servo %i Detached!" % (detached.getSerialNum()))


#HOTFIX!!!!!!!!!!!!!!
#def Error(e):
    #try:
        #source = e.device
    #print("Phidget Error %i: %s %s" % (int(source.getSerialNum()), str(e.eCode), str(e.description))

    #except PhidgetException as e:
        #print("Phidget Exception %i: %s" % (e.code, e.details))

def CurrentChanged(e):
    global currentList
    currentList[e.index] = e.current

def PositionChanged(e):
    source = e.device

def VelocityChanged(e):
    global velocityList
    velocityList[e.index] = e.velocity


def SetupServo(servo_index):
    try :
        print("Setting the servo type for motor %d to HITEC_HS322HD" % servo_index)

        advancedServo.setServoType(servo_index, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)
        #advancedServo.setServoParameters(0, 600, 2000, 120, 1500)

        print("Adjust Velocity Limit to maximum: %f" % advancedServo.getVelocityMax(servo_index))
        advancedServo.setVelocityLimit(servo_index, advancedServo.getVelocityMax(servo_index))

        print("Engage the motor...")
        advancedServo.setEngaged(servo_index, True)

        print("Engaged state: %s" % advancedServo.getEngaged(servo_index))
    except PhidgetException as e :
        print("Phidget Exception %i: %s" % (e.code, e.details))

        try:
                advancedServo.closePhidget()
        except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))

        print("Exiting....")
        exit(1)

# set up event handlers

try :

    advancedServo.setOnAttachHandler(Attached)
    advancedServo.setOnDetachHandler(Detached)
    advancedServo.setOnErrorhandler(Error)
    advancedServo.setOnCurrentChangeHandler(CurrentChanged)
    advancedServo.setOnPositionChangeHandler(PositionChanged)
    advancedServo.setOnVelocityChangeHandler(VelocityChanged)

except PhidgetException as e :

    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)



# create phidget

print("Opening phidget object....")

try :
    advancedServo.openPhidget()
except PhidgetException as e :
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)


# connect to board

print("Waiting for attach....")

try :

    advancedServo.waitForAttach(10000)

except PhidgetException as e:

    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        advancedServo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

else:

    DisplayDeviceInfo()


#Derek Zoolander robot
# servo 0 is right motor, servo 1 is left motor
SetupServo(0)
SetupServo(1)


#function to turn either 90* or 270* right
def turn(right_or_left):

    #turns 90* either 1 or 3 times depending on input
    for i in range(right_or_left):
        advancedServo.setPosition(0, (int(current_speed) - 20))
        time.sleep(5)
        advancedServo.setPosition(0, int(current_speed))
        if right_or_left > 1 :
            time.sleep(5)

#function to control manual steering of robot
def steer(new_angle):
    if 134 < int(new_angle) < 181:
        steer_angle = int(new_angle)
        if steer_angle > 0:
            advancedServo.setPosition(0, int(steer_angle))
            sleep(5)
    elif "x" == new_angle:
        exit(1)
    #else:
        #pass


#function to spin in circles for a user defined time
def dance_for(milliseconds):
    advancedServo.setPosition(0, (180 - int(current_speed)))
    time.sleep(milliseconds)
    advancedServo.setPosition(0, int(current_speed))


current_speed = 90

#run for ever
while(true):

    advancedServo.setPosition(0, int(current_speed))
    advancedServo.setPosition(1, int(current_speed))

    #get mode
    mode_selection = raw_input("Press 's' to set speed, 'r' to turn right,\
     'l' to turn left, 'b' to breakdance,\
      'm' to steer manually, or 'x' to exit:")

    #sets speed to given int
    if "s" == mode_selection:
        new_speed = raw_input("Set forward speed 90-180:")
        if 89 < int(new_speed) < 181:
            current_speed = int(new_speed)
            print("Speed set to %s." % str(current_speed))

        #checks for 'x' to exit
        elif "x" == new_speed:
            exit(1)
        else:
            print("Is %s in between 90 and 180, Hansel?" % str(new_speed))

    #turns 90* using the turn function
    elif "r" == mode_selection:
        turn(1)

    #turns 270* using the turn function
    elif "l" == mode_selection:
        turn(3)

    #spins in circles (i.e. brakdance)
    elif "b" == mode_selection:
        dance_duration = raw_input("How long do you want me to dance for?")
        if int(dance_duration) > 0:
            dance_for(int(dance_duration))
        else:
            print("I can't dance for %s, Hansel." % str(dance_duration))

    #accepts manual speed selection on motor 1
    elif "m" == mode_selection:
        new_angle = raw_input("Set turn speed from 180-135:")
        if 134 < new_angle < 181:
            steer(int(new_angle))
        else:
            print("Is %s in between 135 and 180, Hansel." % str(new_angle))

    #checks for 'x' to exit
    elif "x" == mode_selection:
        print("Relax.")
        exit(1)

    #if someone does not select a real option, yell at them!
    else:
        print("Cool story, Hansel.")

