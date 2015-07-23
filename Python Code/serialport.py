__author__ = 'Manuel'

import serial
import math


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
        self._received = bytearray()

    def send_packet(self, data):

        size = len(data)

        if size > self.packet_size:
            print("Packet too big.")
        else:
            send_size = size | 0xE0
            self.write(bytes([send_size]))
            send_data = bytearray()
            for i, data_byte in enumerate(data):
                send_data.append((data[i] >> 4) | 0xA0)
                send_data.append((data[i] & 0x0F) | 0xA0)

            n_bytes = self.inWaiting()
            while n_bytes <= 0:
                n_bytes = self.inWaiting()

            byte_read = self.read()
            if byte_read[0] == 0x70:
                for i in range(0, size * 2, 2):
                    self.write(send_data[i:i + 2])

                    n_bytes = self.inWaiting()
                    while n_bytes <= 0:
                        n_bytes = self.inWaiting()

                    byte_read = self.read()
                    if byte_read[0] == 0x60:  # TODO: Put all these constants in variables.
                        continue
                    else:
                        pass  # TODO: Something here in case the byte was not received well

    def send_data(self, data):  # TODO: Add timeout

        length = len(data)
        number_packets = int(math.ceil(length / self.packet_size))

        for i in range(0, number_packets):
            n_bytes = self.inWaiting()
            self._received.extend(self.read(n_bytes))
            start_index = i * self.packet_size
            if i < (number_packets - 1):
                self.send_packet(data[start_index:start_index + self.packet_size])
            else:
                self.send_packet(data[start_index:])

    def read_data(self):
        n_bytes = self.inWaiting()
        buffer = self._received[0:]
        buffer.extend(self.read(n_bytes))
        del(self._received[0:])
        return buffer
















