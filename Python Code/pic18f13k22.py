__author__ = 'Manuel'

import serialport as sp
import time
from threading import Thread
from queue import Queue


class ErrorConnection(Exception):

    pass

FIRST_BYTE = 0x55
SECOND_BYTE = 0xDD


class PIC18F13K22:

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
        self.baud_rates = (2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000,
                           1152000, 1500000, 2000000, 2500000, 3000000)

        # PWM stuff
        self.pwm_outputs = ("P1A", "P1B", "P1C", "P1D")  # Make this a Dictionary
        self.pwm_single_mode = ("P1A, P1C active-high; P1B, P1D active-high",
                                "P1A, P1C active-high; P1B, P1D active-low",
                                "P1A, P1C active-low; P1B, P1D active-high",
                                "P1A, P1C active-low; P1B, P1D active-low")

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
        while self._running:
            self._rx_processing(disconnect=disconnect)
            if not self._out_q.empty():
                data = self._out_q.get()
                self.port.send_data(data)

    def _rx_processing(self, disconnect):

        n_bytes = self.port.bytes_in_buffer()

        if n_bytes >= 3:

            self._start_time = time.monotonic()
            self._received_data.extend(self.port.read_data())

            self._check_pic_online()

            self._received_data = self._packet_processing(self._received_data)
            while len(self._received_data) >= 3 and self._running:
                # Check if the packet is complete
                if self._received_data[0] == FIRST_BYTE and self._received_data[1] == SECOND_BYTE:
                    if (self._received_data[2] + 3) > len(self._received_data):
                        break

                self._check_pic_online()
                self._received_data = self._packet_processing(self._received_data)

        elif n_bytes < 3 and self.online:

            end_time = time.monotonic()
            time_dif = (end_time - self._start_time) * 1000
            if time_dif > disconnect and self.online:
                self.online = False
                print("PIC Offline: ", time_dif)

    def _packet_processing(self, received_data):

        length = len(received_data)

        if length >= 3:
            if received_data[0] == FIRST_BYTE and received_data[1] == SECOND_BYTE:

                end_data = received_data[2] + 3
                if length >= end_data:
                    if len(received_data[3:end_data]) > 0:
                        message = received_data[3:end_data]
                        self._message_processing(message)
                    received_data = received_data[end_data:]
            else:
                received_data = received_data[1:]

        return received_data

    def _message_processing(self, message):
        print(message)

    def _check_pic_online(self):
        # If the PIC was offline, This checks for it to be online again.
        if self._received_data[0] == FIRST_BYTE and self._received_data[1] == SECOND_BYTE:
            if not self.online:
                self.online = True
                print("PIC Online")
                del self._received_data[0:]  # TODO: Recheck this code later
                self.port.flushInput()

    def close_connection(self):

        self._running = False
        self.online = False
        if self.port.isOpen():
            while self._t.is_alive():
                pass
            self.port.close()

    def set_pwm(self, value):
        low = value % 4
        high = (value - low) // 4
        data = [0xAC, high, low]
        self._out_q.put(data)

    def pwm_select_output(self, selection, toggle):  # Need to secure later
        outputs_dict = {"P1A": 1, "P1B": 2, "P1C": 4, "P1D": 8}
        out = outputs_dict[selection]
        if toggle:
            self._out_q.put([0xAA, out])
        else:
            self._out_q.put([0xAB, out])