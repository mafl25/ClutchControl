__author__ = 'Manuel'

import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports as ports
from pic18f13k22 import ErrorConnection

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


class CommWidget(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.config(borderwidth=1, relief=tk.RIDGE)

        self.pic = controller.pic

        label1 = tk.Label(self, text="PIC Connection", font=LARGE_FONT)
        label1.grid(row=0, columnspan=3, sticky=(tk.W + tk.E), pady=10, padx=10)  # Check columnspan

        # COM port menu
        self.com = tk.StringVar()
        self.com.set("Choose")
        com_choices = list(ports.comports())
        self.com_menu = ttk.OptionMenu(self, self.com, self.com.get(), *com_choices)
        self.com_menu.grid(row=1, column=1)
        self.com_menu.bind('<Button-1>', self.com_pressed)

        label2 = tk.Label(self, text="Choose Port", font=LARGE_FONT)
        label2.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)

        # Baudrate port menu
        self.rate = tk.IntVar()
        rate_menu = ttk.OptionMenu(self, self.rate, self.pic.baud_rates[8], *self.pic.baud_rates)
        rate_menu.grid(row=2, column=1)

        label3 = tk.Label(self, text="Choose BaudRate", font=LARGE_FONT)
        label3.grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)

        # Warning label
        self.warning = tk.StringVar()
        warning_label = tk.Label(self, font=SMALL_FONT, textvariable=self.warning, width=30,
                                 height=2, justify=tk.LEFT)
        warning_label.grid(row=3, column=0, sticky=tk.W, pady=10, padx=10)

        # Online/Offline label
        self.on_off_line = tk.StringVar()
        self.on_off_line.set("PIC Offline")
        on_off_label = tk.Label(self, font=SMALL_FONT, textvariable=self.on_off_line, width=30,
                                height=2, justify=tk.LEFT)
        on_off_label.grid(row=2, column=2, sticky=tk.W, pady=10, padx=10)
        on_off_label.after(20, update_on_off, on_off_label, self)  # Runs this function every 20 ms
        # What's the point of it being a method? Couldn't I have done this from other widget?

        # Open/Close Button
        self.open_close = tk.StringVar()
        self.open_close.set("Open Port")
        button1 = ttk.Button(self, textvariable=self.open_close, width=15, command=self.open_close_pressed)
        button1.grid(row=1, column=2)

    def open_close_pressed(self):

        if self.open_close.get() == "Open Port":
            port_sel = self.com.get()
            if port_sel.startswith("COM"):
                try:
                    self.pic.open_connection(port=port_sel, baudrate=self.rate.get(), disconnect=500)
                except ErrorConnection as error:
                    print(error)
                    return -1
                self.open_close.set("Close Port")
                self.warning.set("")
            else:
                self.warning.set("No Port Selected")

        else:
            self.pic.close_connection()
            self.open_close.set("Open Port")

        return 0

    def com_pressed(self, event):  # Updates the list of COM ports

        self.com_menu['menu'].delete(0, 'end')
        com_ports = list(ports.comports())

        if len(com_ports) == 0:
            self.com.set("No COM ports detected")
        else:
            for open_ports in com_ports:
                self.com_menu['menu'].add_command(label=open_ports[0], command=tk._setit(self.com, open_ports[0]))


def update_on_off(label, parent):  # Analyze more this function later
    if parent.pic.online:
        parent.on_off_line.set("PIC Online")
    else:
        parent.on_off_line.set("PIC Offline")
    label.after(300, update_on_off, label, parent)  # Have to call it again to kee it running
