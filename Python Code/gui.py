__author__ = 'Manuel'

import tkinter as tk
from tkinter import ttk
from commwidget import CommWidget
from dspic33fj64gp802 import ErrorConnection

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


class ScaleWidget(tk.Frame):

    def __init__(self, parent, controller, row, column, sticky, lower_limit=1, upper_limit=100, resolution=1,
                 call_back=None, tittle=None):

        tk.Frame.__init__(self, parent)
        self.config(borderwidth=1, relief=tk.RIDGE)
        self.grid(row=row, column=column, sticky=sticky)

        self.call_back = call_back

        label1 = tk.Label(self, text=tittle, font=LARGE_FONT)
        label1.grid(row=0, columnspan=2, sticky=(tk.W + tk.E), pady=10, padx=10)

        self.resolution = resolution
        self.scale_value = tk.DoubleVar()
        self.scale_value.set(lower_limit)
        scale = ttk.Scale(self, from_=lower_limit, to=upper_limit, orient=tk.HORIZONTAL, length=450,
                          variable=self.scale_value, command=self.scale_callback)
        scale.grid(row=2, columnspan=2, pady=0, padx=5)
        self.label_var = tk.StringVar()
        scale_label = tk.Label(self, font=SMALL_FONT, textvariable=self.label_var)  # Make a class off of this...
        self.label_var.set(scale.get())

        scale_label.grid(row=3, sticky=tk.W, pady=0, padx=5)

    def scale_callback(self, value):
        int_value = int(self.resolution*round((float(value)/self.resolution)))
        self.label_var.set(int_value)

        if self.call_back:
            self.call_back(value, self.resolution)


class PIDWidget(tk.Frame):
    def __init__(self, parent, controller, row, column, sticky):
        tk.Frame.__init__(self, parent)
        self.config(borderwidth=1, relief=tk.RIDGE)
        self.grid(row=row, column=column, sticky=sticky)

        self.pic = controller.pic

        self.kp = tk.DoubleVar()
        self.ki = tk.DoubleVar()
        self.kd = tk.DoubleVar()
        self.der_toggle_var = tk.IntVar()

        try:
            f = open('parameters', 'r')
            self.kp.set(float(f.readline()))
            self.ki.set(float(f.readline()))
            self.kd.set(float(f.readline()))
            self.der_toggle_var.set(int(f.readline()))
            f.close()
        except:
            self.kp.set(0)
            self.ki.set(0)
            self.kd.set(0)
            self.der_toggle_var.set(int(0))

        label1 = tk.Label(self, text="PID", font=LARGE_FONT)
        label1.grid(row=0, columnspan=5, sticky=(tk.W + tk.E), pady=10, padx=10)

        button1 = ttk.Button(self, width=20, text="Send PID parameters", command=self.send_parameters)
        button1.grid(row=1, column=0, padx=5)

        button2 = ttk.Button(self, width=20, text="Save parameters", command=self.save_parameters)
        button2.grid(row=1, column=1, pady=5, padx=15)

        button3 = ttk.Button(self, width=10, text="Start", command=self.pic.start_pid)
        button3.grid(row=1, column=2, pady=5, padx=15)

        button4 = ttk.Button(self, width=10, text="Stop", command=self.pic.stop_pid)
        button4.grid(row=1, column=3, pady=5, padx=15)

        kp_label = ttk.Label(self, text="KP", font=SMALL_FONT)
        kp_label.grid(row=2, sticky=tk.N, pady=5, padx=5)
        kp_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.kp)
        kp_box.grid(row=3, columnspan=5)

        ki_label = ttk.Label(self, text="KI", font=SMALL_FONT)
        ki_label.grid(row=4, sticky=tk.N, pady=5, padx=5)
        ki_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.ki)
        ki_box.grid(row=5, columnspan=5)

        ki_label = ttk.Label(self, text="KD", font=SMALL_FONT)
        ki_label.grid(row=6, sticky=tk.N, pady=5, padx=5)
        kd_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.kd)
        kd_box.grid(row=7, columnspan=5)

        self.pos_scale = ScaleWidget(parent, controller, row + 1, column, (tk.W + tk.E), 100, 900, 1, self.set_reference,
                                     'PID set point')
        self.pos_scale.grid(columnspan=5)

        box = ttk.Checkbutton(self, text="Derivative Filter", variable=self.der_toggle_var,
                              command=lambda : self.pic.toggle_der_filter(self.der_toggle_var.get()))
        box.grid(row=13)

    def set_reference(self, value, resolution):
        int_value = int(resolution*round((float(value)/resolution)))
        self.pic.set_pos(int_value)

    def save_parameters(self):
        f = open('parameters', 'w')
        f.write(str(self.kp.get()) + '\n')
        f.write(str(self.ki.get()) + '\n')
        f.write(str(self.kd.get()) + '\n')
        f.write(str(self.der_toggle_var.get()) + '\n')
        f.close()

    def send_parameters(self):
        self.pic.set_kp(self.kp.get())
        self.pic.set_ki(self.ki.get())
        self.pic.set_kd(self.kd.get())
        self.pic.toggle_der_filter(self.der_toggle_var.get())


class WindowGUI(tk.Tk):  # This is the base that will help use add frames easily.

    def __init__(self, pic, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)  # I could use super() instead of tk.Tk

        self.pic = pic

        tk.Tk.iconbitmap(self, default="clutch.ico")
        tk.Tk.wm_title(self, "Clutch Control")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0)
        container.grid_columnconfigure(0)

        frame_c = CommWidget(container, self, 0, 0, 'nw', self.pic, ErrorConnection, 500)

        frame_pos = PIDWidget(container, self, 0, 1, 'nw')




