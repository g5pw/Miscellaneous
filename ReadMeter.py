# Packet structure:
# 00 - 0011 0000 - Range
# 01 - 0011 0000 - Digit 4
# 02 - 0011 0000 - Digit 3
# 03 - 0011 0000 - Digit 2
# 04 - 0011 0000 - Digit 1
# 05 - 0011 0000 - Digit 0
# 06 - 0011 1011 - Function
# 07 - 0011 0000 - Status
# 08 - 0011 0000 - Option1
# 09 - 0011 0000 - Option2
# 10 - 0011 1010 - Option3
# 11 - 0011 0000 - Option4
# 12 - 0000 1101 - CR
# 13 - 0000 1010 - LF

import serial, signal

def handler(signum, frame):
    print("Exiting...")

# Open serial port, 7 data bits, even parity, 19230 baud
port = serial.Serial("/dev/cu.SLAB_USBtoUART", 19230, 7, 'E')
signal.signal(signal.SIGTERM, handler)
while True:
    buffer = bytearray(port.read(14))
    if buffer[12] != 0x0D or buffer[13] != 0x0A:
        c = ''
        print "lost sync on " + buffer
        while c != 0x0A:
            c = port.read(1)
            print "Syncing..." + bytearray(c)
        print "Synced!"
    # Get range
    range = (buffer[0] & 0x0F) 
    # Determine mode
    if buffer[6] == 0x30: mode = "A"
    elif buffer[6] == 0x31: mode = "Diode"
    elif buffer[6] == 0x32: mode = "Hz"
    elif buffer[6] == 0x33: mode = "ohm"
    elif buffer[6] == 0x35: mode = "Continuity"
    elif buffer[6] == 0x36: mode = "F"
    elif buffer[6] == 0x3B: mode = "V"
    elif buffer[6] == 0x3D: mode = "uA"
    elif buffer[6] == 0x3F: mode = "mA"
    else:
        mode = ''
        print("Error in determining function: ", hex(buffer[6]))
    if mode == "V" and range == 4:
        range = 2
        mode = "mV"
    elif mode == "F" and range == 0:
        range = 1
        mode = "nF"
    # Digit decoding!
    number  = (buffer[1] & 0x0F)
    number += (buffer[2] & 0x0F) * 10 ** -1
    number += (buffer[3] & 0x0F) * 10 ** -2
    number += (buffer[4] & 0x0F) * 10 ** -3
    number += (buffer[5] & 0x0F) * 10 ** -4
    number *= 10 ** range
    # Check sign!
    if (buffer[7] & 0x04) >> 2:
        number *= -1
    if mode == "ohm" and (buffer[7] & 0x01):
        print "O/L"
    else:
        print number, mode
