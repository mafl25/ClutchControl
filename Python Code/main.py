import pic18f13k22 as mcu
import gui
import sys

__author__ = 'Manuel'


def main():

    pic = mcu.PIC18F13K22(6)
    app = gui.WindowGUI(pic=pic)
    app.mainloop()

    return 0

return_value = main()
sys.exit(return_value)
