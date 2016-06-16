__author__ = 'Manuel'

import serial

port = serial.Serial(port="COM3", baudrate=1000000, timeout=None, rtscts=True)

i = 0
while True:
    n_bytes = port.inWaiting()
    while n_bytes <= 0:
        n_bytes = port.inWaiting()
    byte_2 = port.read(1)
    while n_bytes <= 0:
        n_bytes = port.inWaiting()
    byte_1 = port.read(1)
    while n_bytes <= 0:
        n_bytes = port.inWaiting()
    byte_0 = port.read(1)
    time = (byte_2[0] << 16) | (byte_1[0] << 8) | byte_0[0]
    print(time)

port.close()
