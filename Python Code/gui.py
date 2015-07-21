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

        label2 = tk.Label(self, text="- Select Outputs:", font=SMALL_FONT)
        label2.grid(row=1, sticky=tk.W, pady=5, padx=5)

        self.output_list1 = []
        self.output_list2 = []
        rows = 2
        for i, output in enumerate(self.pic.pwm_outputs):
            self.output_list1.append([tk.IntVar()])
            command_with_args = partial(self.check_selected, i, 1)
            self.output_list1[i].append(ttk.Checkbutton(self, variable=self.output_list1[i][0], text=output,
                                                        command=command_with_args))
            self.output_list1[i][1].grid(row=rows, sticky=tk.W, pady=0, padx=5)

            self.output_list2.append([tk.IntVar()])
            command_with_args = partial(self.check_selected, i, 2)
            self.output_list2[i].append(ttk.Checkbutton(self, variable=self.output_list2[i][0], text=output,
                                                        command=command_with_args))
            self.output_list2[i][1].grid(row=rows, column=1, sticky=tk.E, pady=0, padx=5)
            rows += 1

        # Single Mode Options
        label3 = tk.Label(self, text="- Select Output Mode:", font=SMALL_FONT)
        label3.grid(row=rows, sticky=tk.W, pady=5, padx=5)

        rows += 1
        self.single_output_option = tk.StringVar()
        self.single_output_option.set(self.pic.pwm_single_mode[0])
        self.s_output_mode_menu = ttk.OptionMenu(self, self.single_output_option, self.single_output_option.get(),
                                                 *self.pic.pwm_single_mode)
        self.s_output_mode_menu.grid(row=rows, pady=0, padx=0)
        # self.s_output_mode_menu.bind('<Button-1>', self.com_pressed)

        rows += 1
        label4 = tk.Label(self, text="- PWM Value:", font=SMALL_FONT)
        label4.grid(row=rows, sticky=tk.W, pady=5, padx=5)

        rows += 1
        self.resolution = 10
        self.pw_scale_value = tk.DoubleVar()
        pw_scale = ttk.Scale(self, from_=-1020, to=1020, orient=tk.HORIZONTAL, length=300,
                             variable=self.pw_scale_value, command=self.scale_callback)
        pw_scale.grid(row=rows, columnspan=2, pady=0, padx=5)
        self.var_label_pw = tk.StringVar()
        label_pw = tk.Label(self, font=SMALL_FONT, textvariable=self.var_label_pw)  # Make a class off of this...
        self.var_label_pw.set(pw_scale.get())

        rows += 1
        label_pw.grid(row=rows, sticky=tk.W, pady=0, padx=5)

        rows += 1
        self.go_stop = tk.StringVar()
        self.go_stop.set("GO")
        button1 = ttk.Button(self, textvariable=self.go_stop, width=15, command=self.go_stop_pressed)
        button1.grid(row=rows, columnspan=2, pady=5)

    def check_selected(self, index, column):
        # print(self.output_list1[index][0].get())
        if column != 1 and column != 2:
            return None

        if column == 1:
            if self.output_list1[index][0].get():
                self.output_list2[index][0].set(0)
            if self.go_stop.get() == "STOP":
                value = self.pw_scale_value.get()
                self.scale_set_pwm(value)
        elif column == 2:
            if self.output_list2[index][0].get():
                self.output_list1[index][0].set(0)
            if self.go_stop.get() == "STOP":
                value = self.pw_scale_value.get()
                self.scale_set_pwm(value)

    def go_stop_pressed(self):
        if self.go_stop.get() == "GO":
            self.go_stop.set("STOP")
            value = self.pw_scale_value.get()
            self.scale_set_pwm(value)

        else:
            self.scale_set_pwm(0)
            self.go_stop.set("GO")

    def scale_callback(self, value):
        value = int(self.resolution*round((float(value)/self.resolution)))
        self.var_label_pw.set(value)

        self.scale_set_pwm(value)

    def scale_set_pwm(self, value):
        value = int(self.resolution*round((float(value)/self.resolution)))
        self.var_label_pw.set(value)

        if self.go_stop.get() == "STOP":
            if value < -10:
                for i in range(len(self.output_list1)):
                    if self.output_list1[i][0].get():
                        self.pic.pwm_select_output(self.pic.pwm_outputs[i], 1)
                    else:
                        self.pic.pwm_select_output(self.pic.pwm_outputs[i], 0)
                self.pic.set_pwm(abs(value))
            elif -10 <= value <= 10:
                for i in range(len(self.output_list1)):
                    self.pic.pwm_select_output(self.pic.pwm_outputs[i], 0)
                self.pic.set_pwm(0)
            else:
                for i in range(len(self.output_list2)):
                    if self.output_list2[i][0].get():
                        self.pic.pwm_select_output(self.pic.pwm_outputs[i], 1)
                    else:
                        self.pic.pwm_select_output(self.pic.pwm_outputs[i], 0)
                self.pic.set_pwm(value)