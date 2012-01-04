import serial
import array
import appscript

launchpad = serial.Serial("/dev/tty.uart-12FF41E50F904638", 9600)
itunes = appscript.app('itunes')

wheelPressed = 0

directions = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")

while launchpad.readable():
    buffer = ord(launchpad.read())
    if buffer == 0x80:
	buffer = ord(launchpad.read())
	if buffer == 0x80:
	    print "Center button pressed"
	    itunes.playpause()
    else:
	if buffer == 0xBE:
	    buffer = ord(launchpad.read())
	    if buffer == 0xEF:
		print "Wake up complete!"
	else:
	    if buffer == 0xDE:
		buffer = ord(launchpad.read())
		if buffer == 0xAD:
		    print "Sleep mode!"
	    else:
		if buffer == 0xFC:
		    buffer = ord(launchpad.read())
		    print "Gesture start: " + str(buffer - 0x20)
		else:
		    if buffer == 0xFB:
			buffer = ord(launchpad.read())
			if buffer == 0xFB:
			    print "Gesture stop"
		    else:
			if buffer > 0x30 + 16 or buffer <= 0x20:  #Wheel position offset + number wheel positions
			    continue	    #Invalid data
			else:
			    if (buffer <= 0x30 + 16) and buffer >= 0x30:	#Wheel position here!
				buffer2 = ord(launchpad.read())
				if buffer == buffer2:
				    buffer -= 0x30
				    if wheelPressed == 0:
					wheelPressed = 1
					print "Wheel press: " + directions[buffer]
				    else:
					wheelPressed = 0
					print "Wheel release: " + directions[buffer]
					if buffer == 4:
					    itunes.next_track()
					if buffer == 12:
					    itunes.previous_track()
			    else:						# Gesture here!
				print "Gesture : " + str(buffer-0x20)
