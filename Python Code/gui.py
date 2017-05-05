__author__ = 'Manuel'

import tkinter as tk
from commwidget import CommWidget
from pic18f13k22 import ErrorConnection

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

        frame_c = CommWidget(container, self, self.pic, ErrorConnection)
        frame_c.grid(row=0, column=0, sticky="nw")






