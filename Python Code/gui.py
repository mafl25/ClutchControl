__author__ = 'Manuel'

import tkinter as tk

LARGE_FONT = ("Verdana", 12)


class WindowGUI(tk.Tk):  # This is the base that will help use add frames easily.

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)  # I could use super() instead of tk.Tk
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Empty dictionary, from it, I will be able to store different frames

        frame = StartPage(container, self)

        self.frames[StartPage] = frame  # I add frame to the dictionary, StartPage is the key.

        frame.grid(row=0, column=0, sticky="nsew")
        # Can I use self.frames[StartPage].grid(row=0, column=0, sticky="nsew") instead?

        self.show_frame(StartPage)  # What is this?

    def show_frame(self, cont):

        frame = self.frames[cont]  # This is use to show a different frame. cont is the key to the dict.
        frame.tkraise()  # Raise it to the front


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

app = WindowGUI()
app.mainloop()  # I can do this because WindowGui inherits Tk
