__author__ = 'Manuel'

import serial

port = serial.Serial(port="COM3", baudrate=300000, timeout=None, rtscts=True)

i = 0
while True:
    n_bytes = port.inWaiting()
    read_data = port.read(n_bytes)
    if len(read_data):
        # print(" ".join("%02x" % b for b in read_data))
        print(read_data)
    i += 1
    if i > 100000:
        port.write(bytearray("Manuel", encoding="utf-8"))
        i = 0

port.close()
