import serial
import pylab
import time

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



port = serial.Serial(port="COM3", baudrate=2000000, timeout=2, rtscts=True)
sentence = """It’s been one semester since I came to National Tsing Hua University and it’s been a wonderful experience.
              My time so far in the Power Mechanical Engineering Department has let me meet other wonderful students
              and great professors, as well as learning a great deal from the courses I have taken so far and my work
              in my laboratory. There is, however, much to be done in my time at NTHU, such as continuing my study of
              Chinese and working on my research project for my graduate studies.
              When I arrived at NTHU, I decided to join Prof. James Chang’s Vibrations & Mechatronics Systems
              Laboratory. I have since started my research on variable torque magnetorheological fluid clutches for
              robotic grippers and arms. The objective is to design a small clutch that can be used for compliance in
              the fingers of robotic grippers and arms. So far I have produced several prototypes using 3D printers and
              am currently working on the control system for them. Later on I will have to integrate it with a robotic
              gripper and adapt it to work on a larger system.
              The focus of my master’s degree will be on Micro/Nano and Solid Mechanics, for which I already took
              Sensing and Actuation in Miniaturized Systems and Fabrication and Application of Magnetic Nano Devices
              courses this past semester. For the fall of 2015 semester, I will take the Finite Element Methods and the
              Elasticity courses. On following semesters I will keep taking at least two courses per semester, more if
              they offer several english courses.
              In order to better communicate with my classmates and being able to understand and effectively take more
              courses I will be taking mandarin courses throughout my stay in NTHU. So far I have taken Mandarin Basic I
              and Mandarin Basic Conversation I. For the next semester, I will aim to do the placement test for Mandarin
              Basic II in order to go directly to Mandarin Basic III. 我
              I will forward to the rest of my time at NTHU, as I am sure it will be of great productivity and growth of
              me as a person and will increase my knowledge and abilities as an engineer and future professional."""
data = bytearray(sentence, encoding="utf-8")
port.flushOutput()
port.write(data)


n_bytes = len(data)
print("Data size:", n_bytes)
read_data = port.read(n_bytes)

print(read_data.decode(encoding="utf-8"))
print("Size of received data: ", len(read_data))

if data == read_data:
    print("Test passed.")
else:
    print("Test FAILED!!!")

port.close()



list_of_files = [("""C:\Users\Manuel\Documents\ForPlotting.csv""", "Torque vs Magnet Engagement")]

datalist = [(pylab.loadtxt(filename), label) for filename, label in list_of_files ]

for data, label in datalist:
    pylab.plot(data[:, 0], data[:, 1], label=label )

pylab.legend()
pylab.title("Title of Plot")
pylab.xlabel("X Axis Label")
pylab.ylabel("Y Axis Label")
