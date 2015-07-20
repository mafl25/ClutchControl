__author__ = 'Manuel'

import tkinter as tk
from tkinter import ttk
from commwidget import CommWidget
from functools import partial


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


class PWMWidget(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.config(borderwidth=1, relief=tk.RIDGE)

        self.pic = controller.pic

        label1 = tk.Label(self, text="PWM", font=LARGE_FONT)
        label1.grid(row=0, columnspan=2, sticky=(tk.W + tk.E), pady=10, padx=10)

        label2 = tk.Label(self, text="Choose Output", font=LARGE_FONT)
        label2.grid(row=1, sticky=tk.W, pady=10, padx=10)

        self.output_list = []
        i = 0  # Not really necessary
        for i, output in enumerate(controller.pic.pwm_outputs):
            self.output_list.append([tk.IntVar()])
            command_with_args = partial(self.print_li, i)
            self.output_list[i].append(ttk.Checkbutton(self, variable=self.output_list[i][0], text=output,
                                                       command=command_with_args))
            self.output_list[i][1].grid(row=2 + i, sticky=tk.W, pady=5, padx=5)

        pw_scale = ttk.Scale(self, from_=0, to=1020, orient=tk.HORIZONTAL, length=200, command=self.scale_label)
        pw_scale.grid(row=i + 3, column=0)
        self.var_label_pw = tk.StringVar()
        label_pw = tk.Label(self, font=SMALL_FONT, textvariable=self.var_label_pw)  # Make a class off of this...
        self.var_label_pw.set(pw_scale.get())
        label_pw.grid(row=i + 4, sticky=tk.W, pady=5, padx=5)

    def print_li(self, index):
        print(self.output_list[index][0].get())

    def scale_label(self, value):
        # print(type(value))
        value = int(float(value))
        self.var_label_pw.set(value)
