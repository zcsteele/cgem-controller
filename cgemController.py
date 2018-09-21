# For now this is just a basic test. May want to rename it to something like:
# cgemTest if it actually works.

import convertRaDecToCgemUnits
import serial

import commands

ra  = convertRaDecToCgemUnits.Ra()
dec = convertRaDecToCgemUnits.Dec()

# Setting a 1 second timeout

timeoutValue = 1

# Get and list the possible serial ports

print commands.getstatusoutput ('ls /dev/ttyUSB*')

serialPort = input ("Enter serial port, something like 'ttyUSB0' for example ")

ser = serial.Serial('/dev/'+serialPort, timeout=timeoutValue)
print 'ser name : ', ser.name

# Do a read of the serial port with the idea to clear out
# any characters that may be sitting there.

print 'Do a read of the serial with the timeout of: ', timeoutValue

data = ser.read(50)
print 'data : ', data
loopControl = True

print 'Enter a negative number for the RA hours wnd the loop will exit.'

while loopControl:
    ra.hr   = input ('raHr   : ')

    if ra.hr <= -1:
        print 'User specified time to quit'
        loopControl = False
    else:
        ra.min  = input ('raMin  : ')
        ra.sec  = input ('raSec  : ')
    
        dec.deg = input ('decDeg : ')
        dec.min = input ('decMin : ')
        dec.sec = input ('decSec : ')

        print 'ra  : ', ra.hr,   ra.min,  ra.sec
        print 'dec : ', dec.deg, dec.min, dec.sec
        print

        print 'r'+ra.toCgem()+','+dec.toCgem()

        ser.write ('r'+ra.toCgem()+','+dec.toCgem())

        # Hand controller should respond with a # character

        print 'Changed the timeout value to: ', ser.timeout
        tries = 30
        foundHashTag = False

        while ((tries > 0) or foundHashTag):
            data = ser.read(1)
            print 'data : ', data
            if (data == '#'):
                foundHashTag = True
            tries -= 1
        print

