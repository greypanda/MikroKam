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


def usblist():
    """Detect and report on available USB drives"""

    ulist = []
    removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
    for device in removable:
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        for p in psutil.disk_partitions():
            if p.device in partitions:
                ulist.append(p.mountpoint)
    return ulist


def isWritable(path):
    """Test to see if the usb drive can be written"""
    try:
        testfile = tempfile.TemporaryFile(dir = path)
        testfile.close()
    except OSError as e:
        if e.errno == errno.EACCES:  # 13
            return False
        e.filename = path
        return False
    return True

"""Define some constants
    these will eventually be stored in the config file
"""
TEST_IMAGE = 'test.jpg'
IMAGE_SIZE = (600,400)
PREVIEW_TIMER = 120
class PreviewTask():
    """The preview can run indefinitely ( in theory ) and
        must be able to be terminated. This rather complex
        task insures that the main program keeps control

    """

    def __init__( self, taskFuncPointer ):
        self.__taskFuncPointer_ = taskFuncPointer
        self.__previewThread_ = None
        self.__isRunning_ = False

    def taskFuncPointer( self ) : return self.__taskFuncPointer_

    def isRunning( self ) : 
        return self.__isRunning_ and self.__previewThread_.isAlive()

    def start( self ): 
        if not self.__isRunning_ :
            self.__isRunning_ = True
            self.__previewThread_ = self.previewThread( self )
            self.__previewThread_.start()

    def stop( self ) : self.__isRunning_ = False

    class previewThread( threading.Thread ):
        def __init__( self, bgTask ):      
            threading.Thread.__init__( self )
            self.__bgTask_ = bgTask

        def run( self ):
            #print("running preview thread")
 
            pikamera.Preview()
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


class MainPage:
    """Define the structure of the page
        master is the root or tab
    """
    def __init__( self, master ):
        self.master = master
        self.master.columnconfigure(0,minsize=100)

        self.image = Image.open(TEST_IMAGE)
        self.image = self.image.resize(IMAGE_SIZE,Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.snapimage = Label(master,image=self.photo)
        self.snapimage.grid(row=0,column=0,columnspan=6,rowspan=4,sticky = "NESW")
        self.snapimage.grid_columnconfigure(0,weight=1)
       
        self.SnapshotButton = Button( 
            master, text="Snapshot", command=self.snapshotProcess,bg="light green" )
        self.SnapshotButton.grid(row=0,column=6,columnspan=3,rowspan=1,sticky="NESW")
        self.SnapshotButton.grid_columnconfigure(1,weight=1)

  
        self.PreviewButton = Button( 
            master, text="Preview", command=self.onPreviewClicked )
        self.PreviewButton.grid(row=2,column=6,columnspan=3,rowspan=1,sticky="NESW")
        
        self.usbpath = StringVar()
        self.usbpath.set('No USB drive found')
        self.filePath = Label(master,textvariable = self.usbpath)
        self.filePath.grid(row=5,column=0)
        self.filePath['text'] = self.usbpath

   
        self.cancelButton = Button( 
            master, text="Stop", command=self.onStopClicked )
        self.cancelButton.grid(row=2,column=9,columnspan=4,rowspan=1,sticky="NESW")
       

        self.bgTask2 = PreviewTask( self.previewThread)
      
   
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
                        

    
    def snapshotProcess( self, isRunningFunc=None ) :
        """Process to take a snapshot"""

        """Find a destination for the file
            and insure it is writable

            we only succeed if the is one, and only one drive
        """
        dest = usblist()
        if len(dest) == 0:
            messagebox.showerror('Error','No USB Drive mounted')
            return
        elif len(dest) > 1:
            messagebox.showerror('Error',"Please insert only one USB drive")
            return
 
        path = dest[0]
        if not isWritable(path):
            messagebox.showerror('Error','Cannot write to:' + path)
            return
   
        self.usbpath.set("USB mounted:" + path)

        """Construct the file name"""
        filename = datetime.now().strftime("%Y%m%dT%H%M%SZ") + '.jpeg'
        filepath = path + '/' + filename

        """Invoke the camera"""
        pikamera.Snapshot(filepath )

        """display the last picture and update the label"""
        self.image = Image.open(filepath)
        self.image = self.image.resize((600,427),Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)  
        self.snapimage.configure(image=self.photo)  
        self.usbpath.set("Last snapshot:" + filepath)         
      
        

    def previewThread( self, isRunningFunc=None ) :
        """Start the preview thread and start a timeout"""
        # change the preview button to red to indicate preview is running
        self.PreviewButton["bg"] = "red"

        # disable snapshots to prevent multiple camera access
        self.SnapshotButton.config(state=DISABLED)
        self.SnapshotButton.config(bg='grey')
        
        for i in reversed(range( PREVIEW_TIMER )):
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
            