__author__ = 'Manuel'

import serialport
# from tkinter import *
import sys


def main():

    try:
        port = serialport.MPort(port=3, baudrate=1000000)
    except serialport.MPortOpenError as error:
        print(error)
        return -1

    while 1:
        input_string = input("What do you want to send: ")
        if input_string == "Exit":
            break
        elif input_string == "Hex":
            input_string = input("introduce hex: ")
            data = bytearray.fromhex(input_string)
            port.send_data(data)
        elif input_string == "p":
            print(port.read_data())
        else:
            data = bytearray(input_string, encoding="utf-8")
            port.send_data(data)

    port.close()
    return 0

return_value = main()
sys.exit(return_value)
