__author__ = 'Manuel'

import serial
import math


class SerialException(Exception):
    pass


CTS_CHAR = 0x70
OK_CHAR = 0x60
NOK_CHAR = 0x50
TB_CHAR = 0x40
RX_MASK = 0xA0
RTS_MASK = 0xE0


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
                send_data.append((data[i] >> 4) | RX_MASK)
                send_data.append((data[i] & 0x0F) | RX_MASK)

            n_bytes = self.inWaiting()
            while n_bytes <= 0:
                n_bytes = self.inWaiting()

            byte_read = self.read(n_bytes)
            if byte_read[0] == CTS_CHAR:
                for i in range(0, size * 2, 2):
                    self.write(send_data[i:i + 2])

                    n_bytes = self.inWaiting()
                    while n_bytes <= 0:
                        n_bytes = self.inWaiting()

                    byte_read = self.read(n_bytes)
                    if byte_read[0] == OK_CHAR:
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

    def bytes_in_buffer(self):
        n_bytes = self.inWaiting()
        self._received.extend(self.read(n_bytes))
        return len(self._received)
















