__author__ = 'Manuel'

"""import pic18f13k22 as mcu

pic = mcu.PIC18F13K22(6)
pic.open_connection(port="COM4", baudrate=1000000, disconnect=1000, packet_size=6)
pic.pwm_select_output("P1C", 1)
pic.close_connection()"""

"""import serialport as ser

port = ser.MPort(port="COM4", baudrate=38400, packet_size=6, timeout=0.0)
port.send_data([0xAA, 0x04])
# port.send_data([0xAC, 254, 4])
port.close()
"""

import serial
import time

port = serial.Serial(port="COM4", baudrate=250000, timeout=2, rtscts=True)
sentence = """When I arrived at NTHU, I decided to join Prof. James Chang’s Vibrations & Mechatronics Systems
              Laboratory. I have since started my research on variable torque magnetorheological fluid clutches for
              robotic grippers and arms. The objective is to design a small clutch that can be used for compliance in
              the fingers of robotic grippers and arms. So far I have produced several prototypes using 3D printers and
              am currently working on the control system for them. Later on I will have to integrate it with a robotic
              gripper and adapt it to work on a larger system.

              The focus of my master’s degree will be on Micro/Nano and Solid Mechanics, for which I already took
              Sensing and Actuation in Miniaturized Systems and Fabrication and Application of Magnetic Nano Devices
              courses this past semester. For the fall of 2015 semester, I will take the Finite Element Methods and the
              Elasticity courses. On following semesters I will keep taking at least two courses per semester, more if
              they offer several english courses."""
data = bytearray(sentence, encoding="utf-8")

port.write(data)


n_bytes = len(data)
read_data = port.read(n_bytes)

if data == read_data:
    print("Test passed.")
else:
    print("Test FAILED!!!")

print(read_data.decode(encoding="utf-8"))

port.close()
