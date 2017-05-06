import serial
import time
from threading import Thread
from queue import Queue

__author__ = 'Manuel'


class ErrorConnection(Exception):

    pass

FIRST_BYTE = 0x55
SECOND_BYTE = 0xDD


class dsPIC33FJ64GP802:

    def __init__(self, packet_size):

        # COM port stuff
        self.port = None
        self._t = None
        self.online = False
        self._running = False
        self._received_data = bytearray()
        self._start_time = 0
        self._out_q = Queue()
        self.p_size = packet_size
        self.baud_rates = (2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 300000)
