__author__ = 'Manuel'

import serial

port = serial.Serial(port="COM4", baudrate=300000, timeout=None, rtscts=True)

while True:
    n_bytes = port.inWaiting()
    read_data = port.read(n_bytes)
    if len(read_data):
        print(read_data)

port.close()
