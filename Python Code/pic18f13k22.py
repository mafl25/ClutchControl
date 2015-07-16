__author__ = 'Manuel'

import serialport as sp
import time
# import threading
# from queue import Queue


class ErrorConnection(Exception):

    pass


class PIC18F13K22:

    def __init__(self):

        self.port = None
        self.online = False

    def open_connection(self, port, baudrate=9600, packet_size=15, disconnect=50):

        if packet_size > 15:
            raise ErrorConnection("Packet size too big")
        try:
            self.port = sp.MPort(packet_size=packet_size, port=port, baudrate=baudrate, timeout=0.0)
        except sp.SerialException as error:
            raise ErrorConnection(error.args)

        self.connect_pic(disconnect)

    def connect_pic(self, disconnect):

        received_data = bytearray()
        flag = False

        while True:

            start_time = time.monotonic()
            n_bytes = self.port.inWaiting()
            while n_bytes <= 3:
                n_bytes = self.port.inWaiting()
                end_time = time.monotonic()
                time_dif = (end_time - start_time) * 1000
                if time_dif > disconnect and flag:
                    flag = False
                    self.online = False
                    print("PIC Offline")

            if not flag:
                print("PIC Online")
                flag = True
                self.online = True
                del received_data[0:]
                self.port.flushInput()

            if flag:
                received_data.extend(self.port.read(n_bytes))
                received_data = cut_packet(received_data)
                while len(received_data) >= 3:
                    # Check if the packet is complete
                    if received_data[0] == 0x55 and received_data[1] == 0xDD:
                        if (received_data[2] + 3) > len(received_data):
                            break
                    received_data = cut_packet(received_data)

    def close_connection(self):

        self.port.close()


def cut_packet(received_data):

    length = len(received_data)

    if length >= 3:
        if received_data[0] == 0x55 and received_data[1] == 0xDD:
            # print("Before: ", received_data)
            end_data = received_data[2] + 3
            if length >= end_data:
                # print("After: ", received_data[0:end_data])
                received_data = received_data[end_data:]
                # print("Rest: ", received_data)
        else:
            received_data = received_data[1:]

    return received_data
