__author__ = 'Manuel'

"""import pic18f13k22 as mcu

pic = mcu.PIC18F13K22(6)
pic.open_connection(port="COM4", baudrate=1000000, disconnect=1000, packet_size=6)
pic.pwm_select_output("P1C", 1)
pic.close_connection()"""

import serialport as ser

port = ser.MPort(port="COM4", baudrate=38400, packet_size=6, timeout=0.0)
port.send_data([0xAA, 0x04])
# port.send_data([0xAC, 254, 4])
port.close()
