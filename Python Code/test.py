__author__ = 'Manuel'

# import serial
from serialport import MPort

# port = serial.Serial(port='COM4', baudrate=38400, timeout=0.0)
port = MPort(packet_size=6, port='COM4', baudrate=1000000, timeout=0.0)
data = bytearray("manuel iñárritu fernandez lopez alvarado", encoding="utf-8")
"""size = len(data)

if size <= 6:
    send_size = size | 0xE0
    port.write(bytes([send_size]))
    send_data = bytearray()
    for i, data_byte in enumerate(data):
        send_data.append((data[i] >> 4) | 0xA0)
        send_data.append((data[i] & 0x0F) | 0xA0)
    n_bytes = port.inWaiting()
    while n_bytes <= 0:
        n_bytes = port.inWaiting()
    byte_read = port.read()
    if byte_read[0] == 0x70:
        for i in range(0, size * 2, 2):
            port.write(send_data[i:i + 2])
            n_bytes = port.inWaiting()
            while n_bytes <= 0:
                n_bytes = port.inWaiting()
            byte_read = port.read()
            if byte_read[0] == 0x60:
                continue
            else:
                i -= 2  # or resend"""
port.send_data(data)

print(port.read_data().decode(encoding="utf-8"))

port.close()
