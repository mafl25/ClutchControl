import tkinter as tk
from tkinter import ttk
from projectFonts import LARGE_FONT, SMALL_FONT

__author__ = 'Manuel'


class SpeedWidget(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(borderwidth=1, relief=tk.RIDGE)

        self.pic = controller.pic
        self.previous_error = 0
        self.integral = 0
        self.set_point = 2
        self.kp = tk.DoubleVar()
        self.kp.set(0)
        self.ki = tk.DoubleVar()
        self.ki.set(0)
        self.kd = tk.DoubleVar()
        self.kd.set(0)
        self.setpoint = tk.DoubleVar()
        self.setpoint.set(2)

        self.average = []

        label1 = tk.Label(self, text="Motor Control", font=LARGE_FONT)
        label1.grid(row=0, columnspan=6, sticky=(tk.W + tk.E), pady=10, padx=10)

        self.pwm_value = tk.IntVar()
        self.pwm_value.set(0)
        p_size_entry = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.pwm_value)
        p_size_entry.grid(row=1, columnspan=5)

        button1 = ttk.Button(self, width=5, text="SET", command=lambda: self.pic.set_pwm(self.pwm_value.get()))
        button1.grid(row=2, column=0, padx=5)

        button2 = ttk.Button(self, width=5, text="STOP", command=lambda: self.pic.set_pwm(0))
        button2.grid(row=2, column=3, pady=5, padx=15)

        label_motor_speed = ttk.Label(self, text="Motor Speed:", font=SMALL_FONT)
        label_motor_speed.grid(row=3, sticky=tk.N, pady=5, padx=15)

        self.speed_value = tk.StringVar()

        speed_label = ttk.Label(self, textvariable=self.speed_value, font=SMALL_FONT)
        speed_label.grid(row=4, sticky=tk.N, pady=5, padx=5)

        speed_label.after(63, self.update_label)

        kp_label = ttk.Label(self, text="KP", font=SMALL_FONT)
        kp_label.grid(row=5, sticky=tk.N, pady=5, padx=5)
        kp_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.kp)
        kp_box.grid(row=6, columnspan=5)

        ki_label = ttk.Label(self, text="KI", font=SMALL_FONT)
        ki_label.grid(row=7, sticky=tk.N, pady=5, padx=5)
        ki_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.ki)
        ki_box.grid(row=8, columnspan=5)

        ki_label = ttk.Label(self, text="KD", font=SMALL_FONT)
        ki_label.grid(row=9, sticky=tk.N, pady=5, padx=5)
        kd_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.kd)
        kd_box.grid(row=10, columnspan=5)

        set_point_label = ttk.Label(self, text="Set Point", font=SMALL_FONT)
        set_point_label.grid(row=11, sticky=tk.N, pady=5, padx=5)
        set_point_box = ttk.Entry(self, width=15, justify=tk.CENTER, textvariable=self.setpoint)
        set_point_box.grid(row=12, columnspan=5)

        self.button = tk.IntVar()
        box = ttk.Checkbutton(self, text="PID Toggle", variable=self.button)
        box.grid(row=13)

    def update_label(self):
        if self.pic.motor_speed == "Unknown":
            speed = 0
        else:
            speed = self.pic.motor_speed
        #self.average.append(speed)
        #if len(self.average) > 16:
        #    self.average = self.average[1:]
        #self.speed_value.set("{0:.3f}".format(mean(self.average)))
        self.speed_value.set("{0:.3f}".format(speed))
        if self.button.get():
            self.pid(self.pic.motor_speed, 0.105)
        self.after(105, self.update_label)

    def pid(self, frequency, dt):
        error = self.setpoint.get() - frequency
        print("Error: ", error)
        ki = self.ki.get()
        if ki > 0:
            self.integral += error * dt
            if self.integral * ki > 1023:
                self.integral = 1023 / ki
            if self.integral * ki < -1023:
                self.integral = -1023 / ki

        print("Integral: ", self.integral)
        derivative = (error - self.previous_error)/dt
        self.previous_error = error
        output = error * self.kp.get() + self.integral * ki + derivative * self.kd.get()
        self.pic.set_pwm(int(output))
        print("PWM: ", output)