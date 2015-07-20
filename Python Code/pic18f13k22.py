__author__ = 'Manuel'

import serialport as sp
import time
from threading import Thread
# from queue import Queue


class ErrorConnection(Exception):

    pass


class PIC18F13K22:

    def __init__(self, packet_size):

        # COM port stuff
        self.port = None
        self._t = None
        self.online = False
        self._running = False
        self._online_flag = False
        self.p_size = packet_size

        # PWM stuff
        self.pwm_outputs = ("P1A", "P1B", "P1C", "P1D")  # Make this a Dictionary

    def open_connection(self, port, packet_size, baudrate=9600, disconnect=50):

        if packet_size > self.p_size:
            raise ErrorConnection("Packet size too big")
        try:
            self.port = sp.MPort(packet_size=packet_size, port=port, baudrate=baudrate, timeout=0.0)
        except sp.SerialException as error:
            raise ErrorConnection(error.args)

        self._t = Thread(target=self._connect_pic, args=(disconnect,), daemon=True)
        self._running = True
        self._t.start()

    def _connect_pic(self, disconnect):

        received_data = bytearray()
        self._online_flag = False

        while self._running:

            start_time = time.monotonic()
            n_bytes = self.port.inWaiting()
            while n_bytes <= 3 and self._running:
                n_bytes = self.port.inWaiting()
                end_time = time.monotonic()
                time_dif = (end_time - start_time) * 1000
                if time_dif > disconnect and self._online_flag:
                    self._online_flag = False
                    self.online = False

            received_data.extend(self.port.read(n_bytes))
            received_data = self.cut_packet(received_data)
            while len(received_data) >= 3:
                # Check if the packet is complete
                if received_data[0] == 0x55 and received_data[1] == 0xDD:
                    if (received_data[2] + 3) > len(received_data):
                        break
                received_data = self.cut_packet(received_data)

    def close_connection(self):

        self._running = False
        self.online = False
        if self.port.isOpen():
            while self._t.is_alive():
                pass
            self.port.close()

    # def set_pwm(self, value):

    def cut_packet(self, received_data):

        length = len(received_data)

        if length >= 3:
            if received_data[0] == 0x55 and received_data[1] == 0xDD:

                if not self._online_flag:
                    self._online_flag = True
                    self.online = True
                    del received_data[0:]
                    self.port.flushInput()
                    return received_data

                end_data = received_data[2] + 3
                if length >= end_data:
                    if len(received_data[3:end_data]) > 0:
                        message = received_data[3:end_data]
                        print(message)
                    received_data = received_data[end_data:]
            else:
                received_data = received_data[1:]

        return received_data
