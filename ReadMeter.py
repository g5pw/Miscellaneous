# Packet structure:
# 00 - 1011 0000 - Range
# 01 - 1011 0000 - Digit 4
# 02 - 1011 0000 - Digit 3
# 03 - 1011 0000 - Digit 2
# 04 - 1011 0000 - Digit 1
# 05 - 1011 0000 - Digit 0
# 06 - 0011 1011 - Voltage
# 07 - 1011 0000
# 08 - 1011 0000
# 09 - 1011 0000
# 10 - 1011 1010
# 11 - 1011 0000
# 12 - 0000 1101
# 13 - 1000 1010

import serial

ser = serial.Serial("/dev/cu.SLAB_USBtoUART", 19230, 7, 'E')

while True:
    buffer = bytearray(ser.read(14))
    if buffer[12] != 13:
        c = ''
        print "lost sync on " + buffer.encode("hex")
        while c != 0x0D:
            c = decode(ser.read(1))
            print "Syncing..." + hex(c)
        print "Synced!"
        ser.read(1) #Read last bit
    # Digit decoding!
    range  = 0
    digit4 = (buffer[1] & 0x0F) * 10 ** (range)
    digit3 = (buffer[2] & 0x0F) * 10 ** (range-1)
    digit2 = (buffer[3] & 0x0F) * 10 ** (range-2)
    digit1 = (buffer[4] & 0x0F) * 10 ** (range-3)
    digit0 = (buffer[5] & 0x0F) * 10 ** (range-4)
    number = digit0 + digit1 + digit2 + digit3 + digit4
    # Check sign!
    if (buffer[7] & 0x04) >> 2:
        number *= -1
    print number
