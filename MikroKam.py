#! /usr/bin/env python3
"""MikroKam

MikroKam is a Python application using tkinter.

It requires a Raspberry Pi 3 (maybe a 2 will work), a camera
plugged into the CSI port, the Rpi touchscreen and Raspbian.

It only runs on Python 3

version 0.1.0 -- first release, the none tabbed version

"""
import threading
from tkinter import Tk, Label, Button, StringVar, FALSE
from time import sleep
from tkinter.ttk import Notebook,Frame,LabelFrame
from mainpage import MainPage

__version__ = '0.1.0'

def is_pi():
    """Detect a Pi, using GPIO module
    """
    try:
        import RPi.GPIO
        return True
    except:
        return False


def Main():
    """Set up the environment and run the main loop
    """
    root = Tk() 
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.title( "MikroKam" )
    if is_pi():
        """Use the whole screen if native"""
        root.geometry('%dx%d+%d+%d' % (ws,hs-80,0,0 ))
    else:
        """For development desktop, simulate the Rpi touchscreen"""
        root.geometry('800x480+0+0')
    root.resizable(width=FALSE,height=FALSE)
    
   
    
    mainPage = Frame(root)
    mainPage.grid(row=0,column=0)
    mainPage.minsize = ws
    
    gui = MainPage( mainPage ) 
   
    print(ws,hs)
    root.protocol( "WM_DELETE_WINDOW", gui.close )
    
    root.mainloop()

if __name__ == "__main__": 
     Main()

            