"""Auto Update
"""
from flashman import FlashMan
import importlib.util
from tkinter import Tk, TOP,BOTH,YES,CENTER,BOTTOM,NO
from tkinter.ttk import Notebook,Frame,LabelFrame,Label,Button

class AutoUpdate():
    def __init__(self):
        self.auto = FlashMan(None)
        self.path = ''
        self.root = Tk()

        #sp = SplashScreen(self.root)
        #sp.config(background="#3366ff")

        #m = Label(sp, text="This is a test of the splash screen\n\n\nThis is only a test.\nwww.sunjay-varma.com")
        #m.pack(side=TOP, expand=NO)
        #m.config(bg="#3366ff",  font=("calibri", 29))
        
        #Button(sp, text="Press this button to kill the program",  command=self.root.destroy).pack(side=BOTTOM)
        #self.root.mainloop()
    def find_update(self):
        drives = self.auto.usblist()
        if len(drives) != 1:
            print("no drive found")
            return False
        try:
            self.path = drives[0] + '/MikroKamupdate.py' 
            with open(self.path,'r'):
                print("update found")
        except:
            print("No update file found")
            return False
        return True
    def execute_update(self):
        print("executing update")
        spec = importlib.util.spec_from_file_location("update.py",self.path)
        update = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(update)
        go = update.UpdateClass()
        go.update()
        return True

        pass

class SplashScreen(Frame):
    def __init__(self, master=None, width=0.8, height=0.6, useFactor=True):
        Frame.__init__(self, master)
        self.pack()

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2) 
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (300, 300, 100,100))
        
        self.master.overrideredirect(True)
        self.lift()
