__author__ = 'Manuel'

import serialport


class ErrorConnection(Exception):

    pass


class PIC18F13K22:

    def __init__(self):

        self.port = None

    def open_connection(self, port, baudrate=9600, packet_size=15):

        if packet_size > 15:
            raise ErrorConnection("Packet size too big")

        try:
            self.port = serialport.MPort(port, baudrate, packet_size)
        except serialport.MPortOpenError as error:
            raise ErrorConnection(error.args())

    def close_connection(self):

        self.port.close()
