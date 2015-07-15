__author__ = 'Manuel'

import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports as ports


LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


class WindowGUI(tk.Tk):  # This is the base that will help use add frames easily.

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)  # I could use super() instead of tk.Tk

        tk.Tk.iconbitmap(self, default="clutch.ico")
        tk.Tk.wm_title(self, "Clutch Control")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Empty dictionary, from it, I will be able to store different frames

        for F in (StartPage,):  # Is just calling the name of a class like calling a function?
                                        # Is F here just a function

            frame = F(container, self)

            self.frames[F] = frame  # I add frame to the dictionary, StartPage is the key.

            frame.grid(row=0, column=0, sticky="nsew")
            # Can I use self.frames[StartPage].grid(row=0, column=0, sticky="nsew") instead?

        self.show_frame(StartPage)  # What is this?

    def show_frame(self, cont):

        frame = self.frames[cont]  # This is use to show a different frame. cont is the key to the dict.
        frame.tkraise()  # Raise it to the front


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="PIC Connection", font=LARGE_FONT)
        label1.grid(row=0, columnspan=2, sticky=(tk.W + tk.E), pady=10, padx=10)

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
        rate_choices = [2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000,
                        1152000, 1500000, 2000000, 2500000, 3000000]
        rate_menu = ttk.OptionMenu(self, self.rate, rate_choices[12], *rate_choices)
        rate_menu.grid(row=2, column=1)

        label3 = tk.Label(self, text="Choose BaudRate", font=LARGE_FONT)
        label3.grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)

        # Packet Size entry
        self.p_size = tk.IntVar()
        self.p_size.set(15)
        p_size_entry = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.p_size)
        p_size_entry.grid(row=3, column=1)

        label4 = tk.Label(self, text="Choose Packet Size", font=LARGE_FONT)
        label4.grid(row=3, column=0, sticky=tk.W, pady=10, padx=10)

        self.warning = tk.StringVar()
        warning_label = tk.Label(self, text="", font=SMALL_FONT, textvariable=self.warning, width=30,
                                 height=2, justify=tk.LEFT)
        warning_label.grid(row=4, column=0, sticky=tk.W, pady=10, padx=10)

        # Open/Close Button
        self.open_close = tk.StringVar()
        self.open_close.set("Open Port")
        button1 = ttk.Button(self, textvariable=self.open_close, width=15, command=self.open_close_pressed)
        button1.grid(row=1, column=2)

    def open_close_pressed(self):

        # Gets the value of the packet size
        try:
            size = self.p_size.get()
            if 0 < size <= 15:
                self.warning.set("")
            else:
                self.warning.set("Value of the packet size must be an\ninteger between 1 and 15.")
        except ValueError:
            self.warning.set("Please enter an integer between 1\nand 15 in the \"Packet Size\" entry.")

        # Change later
        # Open or closes the connection with the pic.
        if self.open_close.get() == "Open Port":
            port_sel = self.com.get()
            if port_sel.startswith("COM"):
                print(port_sel)
                self.open_close.set("Close Port")
            else:
                print("No Port Selected")  # Fluff while I get the real thing.
        else:
            print("Port Closed")
            self.open_close.set("Open Port")

    def com_pressed(self, event):  # Updates the list of COM ports

        self.com_menu['menu'].delete(0, 'end')
        com_ports = list(ports.comports())

        if len(com_ports) == 0:
            self.com.set("No COM ports detected")
        else:
            for open_ports in com_ports:
                self.com_menu['menu'].add_command(label=open_ports[0], command=tk._setit(self.com, open_ports[0]))


app = WindowGUI()
app.mainloop()  # I can do this because WindowGui inherits Tk
