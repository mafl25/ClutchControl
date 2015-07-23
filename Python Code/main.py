__author__ = 'Manuel'


import pic18f13k22 as PIC
import gui
import sys


def main():

    pic = PIC.PIC18F13K22(6)
    app = gui.WindowGUI(pic=pic)
    app.mainloop()

    return 0

return_value = main()
sys.exit(return_value)
