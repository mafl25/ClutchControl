__author__ = 'Manuel'

import tkinter as tk
from tkinter import ttk
from commwidget import CommWidget
from pwmwidget import PWMWidget


LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


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

        frame_c = CommWidget(container, self)
        frame_c.grid(row=0, column=0, sticky="nw")

        frame_pwm = PWMWidget(container, self)
        frame_pwm.grid(row=0, column=1, sticky="nw")

        frame_pwm = StepperWidget(container, self)
        frame_pwm.grid(row=0, column=2, sticky="nw")


class StepperWidget(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(borderwidth=1, relief=tk.RIDGE)

        self.pic = controller.pic

        label1 = tk.Label(self, text="Stepper Motor", font=LARGE_FONT)
        label1.grid(row=0, columnspan=5, sticky=(tk.W + tk.E), pady=10, padx=10)

        self.steps = tk.IntVar()
        self.steps.set(1)
        p_size_entry = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.steps)
        p_size_entry.grid(row=1, columnspan=5)

        button1 = ttk.Button(self, width=5, text="<<",command=self.pic.stepper_move_backward)
        button1.grid(row=2, column=0, pady=5)

        button2 = ttk.Button(self, width=5, text="<",
                             command=lambda: (self.pic.stepper_step_backward(self.steps.get())))
        button2.grid(row=2, column=1, pady=5)

        button3 = ttk.Button(self, width=5, text=">",
                             command=lambda: (self.pic.stepper_step_forward(self.steps.get())))
        button3.grid(row=2, column=3, pady=5)

        button4 = ttk.Button(self, width=5, text=">>", command=self.pic.stepper_move_forward)
        button4.grid(row=2, column=4, pady=5)

        self.stepper_scale_resolution = 1
        self.stepper_freq_scale_value = tk.DoubleVar()
        pw_scale = ttk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, length=200,
                             variable=self.stepper_freq_scale_value, command=self.scale_callback)
        pw_scale.grid(row=3, columnspan=5, pady=0, padx=0)
        self.var_label_stepper = tk.StringVar()
        label_stepper_freq = tk.Label(self, font=SMALL_FONT, textvariable=self.var_label_stepper)
        self.var_label_stepper.set(pw_scale.get())

        label_stepper_freq.grid(row=4, sticky=tk.W, pady=0, padx=5)

    def scale_callback(self, value):
        value = int(self.stepper_scale_resolution*round((float(value)/self.stepper_scale_resolution)))
        self.var_label_stepper.set(value)
        self.pic.set_stepper_interval(value)
