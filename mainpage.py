"""MikroCam main page

    provides the main (or only) application page.

    This can be used as the only page, or one of
    several pages in a notebook. No changes are
    required.
"""


import threading
import pikamera
import pyudev
import psutil
context = pyudev.Context()
import tempfile
import errno







"""Define some constants
    these will eventually be stored in the config file
"""

class PreviewTask():
    """The preview can run indefinitely ( in theory ) and
        must be able to be terminated. This rather complex
        task insures that the main program keeps control

    """

    def __init__( self, taskFuncPointer,config ):
        self.__taskFuncPointer_ = taskFuncPointer
        self.__previewThread_ = None
        self.__isRunning_ = False
        self.config = config

    def taskFuncPointer( self ) : return self.__taskFuncPointer_

    def isRunning( self ) : 
        return self.__isRunning_ and self.__previewThread_.isAlive()

    def start( self ): 
        if not self.__isRunning_ :
            self.__isRunning_ = True
            self.__previewThread_ = self.previewThread( self,self.config )
            self.__previewThread_.start()

    def stop( self ) : self.__isRunning_ = False

    class previewThread( threading.Thread ):
        def __init__( self, bgTask ,config):      
            threading.Thread.__init__( self )
            self.__bgTask_ = bgTask
            self.config = config

        def run( self ):
            #print("running preview thread")
 
            pikamera.Preview(self.config)
            try :
                self.__bgTask_.taskFuncPointer()( self.__bgTask_.isRunning )
            except Exception as e:
                 print( repr(e))
            self.__bgTask_.stop()
            #print("ending preview thread")
            pikamera.Stop()


from tkinter import Tk, Label, Button, StringVar, IntVar, NORMAL, DISABLED, messagebox
from time import sleep
from datetime import datetime
from tkinter.ttk import Notebook,Frame, Checkbutton
from PIL import Image, ImageTk
from flashman import FlashMan

class MainPage:
    """Define the structure of the page
        master is the root or tab
        TEST_IMAGE = 'test.jpg'
        IMAGE_SIZE = (600,400)
        PREVIEW_TIMER = 120
    """
    def __init__( self, master,config,root ):
        self.root = root
        self.flashman = FlashMan(master)
        self.config = config
        self.master = master
        self.master.columnconfigure(0,minsize=100)

        self.image = Image.open(self.config['app']['test_image'])
        self.image = self.image.resize((int(self.config['app']['photo_width']),
                                        int(self.config['app']['photo_height']))
                                        ,Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.snapimage = Label(master,image=self.photo)
        self.snapimage.grid(row=0,column=0,columnspan=6,rowspan=4,sticky = "NESW")
        self.snapimage.grid_columnconfigure(0,weight=1)
       
        self.SnapshotButton = Button( 
            master, text="Snapshot", command=self.snapshotProcess,bg="light green" )
        self.SnapshotButton.grid(row=0,column=6,columnspan=6,rowspan=1,sticky="NESW")
        self.SnapshotButton.grid_columnconfigure(1,weight=1)

  
        self.PreviewButton = Button( 
            master, text="Preview", command=self.onPreviewClicked )
        self.PreviewButton.grid(row=2,column=6,columnspan=6,rowspan=1,sticky="NESW")
        
        self.usbpath = StringVar()
        self.usbpath.set('No USB drive found')
        self.filePath = Label(master,textvariable = self.usbpath)
        self.filePath.grid(row=5,column=0)
        self.filePath['text'] = self.usbpath

   
        self.cancelButton = Button( 
            master, text="Stop", command=self.onStopClicked )
        self.cancelButton.grid(row=2,column=13,columnspan=6,rowspan=1,sticky="NESW")
       
        self.quitButton = Button(
            master,text="Quit",command=self.onQuitClicked)
        self.quitButton.grid(row=4,column=9,columnspan=4,rowspan=1,sticky="NESW")

        self.bgTask2 = PreviewTask( self.previewThread,self.config)
      
   
    def close( self ) :
        print( "close")
        try: self.bgTask.stop()
        except: pass
        try: self.bgTask2.stop()
        except: pass
         
        self.master.quit()

    def onPreviewClicked( self ):
        """The preview button was clicked"""
        print ("onPreviewClicked")
        try: self.bgTask2.start()
        except: pass

  
    def onStopClicked( self ) :
        """The stop button was clicked"""
        print ("onStopClicked")
        try: self.bgTask2.stop()
        except: pass
                        
    def onQuitClicked(self):
        """the quit button was clicked"""
        print("on quit clicked")
        self.close()
        try:
           
            self.root.destroy()
        except:
            print('oops')
            pass
    def snapshotProcess( self, isRunningFunc=None ) :
        """Process to take a snapshot"""

        """Find a destination for the file
            and insure it is writable

            we only succeed if the is one, and only one drive
        """
        dest = self.flashman.usblist()
        if len(dest) == 0:
            messagebox.showerror('Error','No USB Drive mounted')
            return
        elif len(dest) > 1:
            messagebox.showerror('Error',"Please insert only one USB drive")
            return
 
        path = dest[0]
        if not self.flashman.isWritable(path):
            messagebox.showerror('Error','Cannot write to:' + path)
            return
   
        self.usbpath.set("USB mounted:" + path)

        """Construct the file name"""
        #filename = datetime.now().strftime("%Y%m%dT%H%M%SZ") + '.jpeg'
        ##filepath = path + '/' + filename

        current_photo = self.config['app']['photo_count_current']
        if not current_photo:
            self.config['app']['photo_count_current'] = self.config['app']['photo_count_initial']
            current_photo = self.config['app']['photo_count_current']
        filepath = path + '/' + self.config['app']['photo_prefix'] + current_photo  + '.' + self.config['camera']['capture_format']

        """Invoke the camera"""
        pikamera.Snapshot(self.config,filepath )

        """display the last picture and update the label"""
        self.image = Image.open(filepath)
        self.image = self.image.resize((int(self.config['app']['photo_width']),int(self.config['app']['photo_height'])),Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)  
        self.snapimage.configure(image=self.photo)  
        self.usbpath.set("Last snapshot:" + filepath) 
        cp = int(current_photo) 
        cp += 1
        self.config['app']['photo_count_current'] = str(cp)
        with open('MikroKam.ini','w') as configfile:
            self.config.write(configfile) 
        self.config.read('MikroKam.ini')     
      
        

    def previewThread( self, isRunningFunc=None ) :
        """Start the preview thread and start a timeout"""
        # change the preview button to red to indicate preview is running
        self.PreviewButton["bg"] = "red"

        # disable snapshots to prevent multiple camera access
        self.SnapshotButton.config(state=DISABLED)
        self.SnapshotButton.config(bg='grey')
        
        for i in reversed(range(int(self.config['preview']['duration'])) ):
            try:
                if not isRunningFunc() :
                    self.PreviewButton["bg"] ='light blue' 
                    self.SnapshotButton.config(state=NORMAL)
                    self.SnapshotButton.config(bg='light green')

                    return
            except : pass   

       #     print(i)
            sleep( 1.0 ) 

        # restore the buttons
        self.SnapshotButton.config(state=NORMAL)
        self.PreviewButton['bg'] = 'light blue'
                     
   


if __name__ == "__main__":
    print("Requires MikroKam")
    sys.exit()
            