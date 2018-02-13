"""pikamera is an encapsulation of picamera

    It only does three things:
        Starts a preview
        Stops a preview
        Take a snapshot

    If it is not running on a Pi, it just pretends to work
#"""
try:
    from picamera import PiCamera
    CAMERA = 'pi'
except:
    CAMERA = 'pseudo'
from time import sleep
import shutil

if CAMERA == 'pi':
    camera = PiCamera()
def Snapshot(path):
    if CAMERA == 'pi':
       
        camera.start_preview(fullscreen=False,window=(10,10,600,400))
        sleep(2)
        camera.capture(path)
        camera.stop_preview()
    else:
        shutil.copyfile('sample.jpg',path)

def Preview():
    if CAMERA == 'pi':
       
        camera.start_preview(fullscreen=False,window=(10,10,600,400))
    
def Stop():
    if CAMERA == 'pi':
        camera.stop_preview()

