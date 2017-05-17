import dspic33fj64gp802 as mcu
import gui
import sys

__author__ = 'Manuel'


def main():

    pic = mcu.dsPIC33FJ64GP802(6)
    app = gui.WindowGUI(pic=pic)
    app.mainloop()

    return 0

return_value = main()
sys.exit(return_value)
