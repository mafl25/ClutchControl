__author__ = 'Manuel'

import serial
import math


class MPortOpenError(Exception):

    pass


class MPort(object):

    def __init__(self, port, baudrate=9600, packet_size=15, timeout=0.0):

        try:
            self.port = serial.Serial(port=port, baudrate=baudrate, stopbits=serial.STOPBITS_TWO,
                                      timeout=timeout)
        except serial.SerialException:
            raise MPortOpenError("COM{0} could not be opened".format(port + 1))

        self.port.setRTS(False)
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

            self.port.setRTS(True)
            while not self.port.getCTS():  # Waits until the MCU is ready to receive data
                pass

            self.port.write(packet)

            while self.port.getCTS():  # Waits until the MCU received the data
                pass
            self.port.setRTS(False)

    def send_data(self, data):

        length = len(data)
        number_packets = int(math.ceil(length / self.packet_size))

        for i in range(0, number_packets):
            start_index = i * self.packet_size
            if i < (number_packets - 1):
                self.send_packet(data[start_index:start_index + self.packet_size])
            else:
                self.send_packet(data[start_index:])

    def read_data(self, num_bytes):

        if num_bytes < 1:
            number = self.port.inWaiting()
        else:
            number = num_bytes
        buffer = self.port.read(number)
        self.data.extend(buffer)
        buffer = self.data[0:]
        del self.data[0:]
        return buffer

    def open(self):

        self.port.open()

    def close(self):

        self.port.close()














