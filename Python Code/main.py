__author__ = 'Manuel'

# import serialport
# from tkinter import *
import pic18f13k22 as PIC
import sys


def main():

    pic = PIC.PIC18F13K22()
    try:
        pic.open_connection(3, baudrate=38400)
    except PIC.ErrorConnection as error:
        print(error)
        return -1

    while 1:
        pic.print_pic()

    pic.close_connection()
    return 0

return_value = main()
sys.exit(return_value)
