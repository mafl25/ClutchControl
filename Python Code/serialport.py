__author__ = 'Manuel'

import serial
import math
import time


class SerialException(Exception):
    pass


class MPort(serial.Serial):

    def __init__(self, packet_size, *args, **kwargs):

        try:
            serial.Serial.__init__(self, *args, **kwargs)
        except serial.SerialException as error:
            raise SerialException(error.args)
        self.setRTS(False)
        self.data = bytearray()
        self.packet_size = packet_size

    def send_packet(self, data):

        packet = bytearray(1)
        size = len(data)

        if size > self.packet_size:
            print("Packet too big.")
        else:
            packet[0] = size
            packet.extend(data)

            self.setRTS(True)
            while not self.getCTS():  # Waits until the MCU is ready to receive data
                pass

            self.write(packet)
            print(packet)

            while self.getCTS():  # Waits until the MCU received the data
                pass
            self.setRTS(False)

    def send_data(self, data):  # Add timeout

        length = len(data)
        number_packets = int(math.ceil(length / self.packet_size))

        for i in range(0, number_packets):
            start_index = i * self.packet_size
            if i < (number_packets - 1):
                self.send_packet(data[start_index:start_index + self.packet_size])
            else:
                self.send_packet(data[start_index:])















