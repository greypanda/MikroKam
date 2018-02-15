#! /usr/bin/env python3
"""MikroKam

MikroKam is a Python application using tkinter.

It requires a Raspberry Pi 3 (maybe a 2 will work), a camera
plugged into the CSI port, the Rpi touchscreen and Raspbian.

It only runs on Python 3

version 0.1.0 -- first release, the none tabbed version
version 0.2.0 -- 
                    changed file naming to internal counter
                    moved usb to new module -- flashman



"""
import threading
from tkinter import Tk, Label, Button, StringVar, FALSE, messagebox
from time import sleep
from tkinter.ttk import Notebook,Frame,LabelFrame
from mainpage import MainPage
import configparser
import datetime
from autoupdate import AutoUpdate

from flashman import FlashMan


root = Tk()

__version__ = '0.2.0'

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
#    auto = AutoUpdate()
#    if auto.find_update():
#        if auto.execute_update():
#            print("reloading ourself")
   
    config = configparser.ConfigParser()
    config.read('MikroKam.ini')
   
   
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.title( "MikroKam" )
    if is_pi():
        """Use the whole screen if native"""
        root.geometry('%dx%d+%d+%d' % ( int(config['app']['screen_width']),
                                        int(config['app']['screen_height']),0,0 ))
    else:
        """For development desktop, simulate the Rpi touchscreen"""
        root.geometry('800x480+0+0')
    root.resizable(width=FALSE,height=FALSE)
    
   
    
    mainPage = Frame(root)
    mainPage.grid(row=0,column=0)
    mainPage.minsize = ws
    
    gui = MainPage( mainPage,config,root ) 
   
    print(ws,hs)
    root.protocol( "WM_DELETE_WINDOW", gui.close )
   
    root.mainloop()
    print("we are done")
    config['app']['last_run'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('MikroKam.ini','w') as configfile:
        config.write(configfile) 

if __name__ == "__main__": 
     Main()

            