__author__ = 'Manuel'

import serialport
import threading
from queue import Queue


class ErrorConnection(Exception):

    pass


class PIC18F13K22:

    def __init__(self):

        self.port = None

    def open_connection(self, port, baudrate=9600, packet_size=15):

        if packet_size > 15:
            raise ErrorConnection("Packet size too big")
        try:
            self.port = serialport.MPort(port, baudrate, packet_size, timeout=0.0)
        except serialport.MPortOpenError as error:
            raise ErrorConnection(error.args)

    def print_pic(self):
        received_data = bytearray()
        received_data.extend(self.port.read_data(15))
        length = len(received_data)
        while length == 0:
            received_data.extend(self.port.read_data(15))
            length = len(received_data)
        if length > 3:
            if received_data[0] == 0x55 and received_data[1] == 0xDD:
                size_data = received_data[2]
                if length >= (size_data + 3):
                    print("Lom")
                    print(received_data)
                    received_data = received_data[size_data + 3:]  # need to put the actual data in another buffer
                    print(received_data)

    def close_connection(self):

        self.port.close()
