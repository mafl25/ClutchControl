import tkinter as tk
from tkinter import ttk
from projectFonts import LARGE_FONT, SMALL_FONT

__author__ = 'Manuel'


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

        button1 = ttk.Button(self, width=5, text="<<",command=self.move_backward)
        button1.grid(row=2, column=0, pady=5)

        button2 = ttk.Button(self, width=5, text="<",
                             command=lambda: (self.step_backward(self.steps.get())))
        button2.grid(row=2, column=1, pady=5)

        button3 = ttk.Button(self, width=5, text=">",
                             command=lambda: (self.step_forward(self.steps.get())))
        button3.grid(row=2, column=3, pady=5)

        button4 = ttk.Button(self, width=5, text=">>", command=self.move_forward)
        button4.grid(row=2, column=4, pady=5)

        self.stepper_scale_resolution = 1
        self.stepper_freq_scale_value = tk.DoubleVar()
        self.stepper_freq_scale_value.set(1)
        pw_scale = ttk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, length=200,
                             variable=self.stepper_freq_scale_value, command=self.scale_callback)
        pw_scale.grid(row=3, columnspan=5, pady=0, padx=0)
        self.var_label_stepper = tk.StringVar()
        label_stepper_freq = tk.Label(self, font=SMALL_FONT, textvariable=self.var_label_stepper)
        self.var_label_stepper.set(pw_scale.get())

        label_stepper_freq.grid(row=4, sticky=tk.W, pady=0, padx=5)

        label_magnet = tk.Label(self, text="Magnet Position:", font=SMALL_FONT)
        label_magnet.grid(row=4, columnspan=5, sticky=tk.W, pady=10, padx=10)

        self.stepper_position = tk.StringVar()
        label_magnet_position = tk.Label(self, textvariable=self.stepper_position, font=SMALL_FONT)
        label_magnet_position.grid(row=5, columnspan=5, sticky=tk.W, pady=0, padx=10)
        label_magnet_position.after(10, self.update_position)

    def update_position(self):
        self.stepper_position.set(self.pic.stepper_position)
        self.after(10, self.update_position)

    def move_forward(self):
        self.scale_callback(self.stepper_freq_scale_value.get())
        self.pic.stepper_move_forward()

    def move_backward(self):
        self.scale_callback(self.stepper_freq_scale_value.get())
        self.pic.stepper_move_backward()

    def step_forward(self, value):
        self.scale_callback(self.stepper_freq_scale_value.get())
        self.pic.stepper_step_forward(value)

    def step_backward(self, value):
        self.scale_callback(self.stepper_freq_scale_value.get())
        self.pic.stepper_step_backward(value)

    def scale_callback(self, value):
        value = int(self.stepper_scale_resolution*round((float(value)/self.stepper_scale_resolution)))
        self.var_label_stepper.set(value)
        self.pic.set_stepper_interval(value)