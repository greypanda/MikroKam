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
def Snapshot(config,path):
    if CAMERA == 'pi':
        camera.resolution = (int(config['app']['resolution_width']),int(config['app']['resolution_height']))
        camera.start_preview(fullscreen=False,window=(int(config['app']['pvw_left_margin']),
                                                    int(config['app']['pvw_top_margin']),
                                                    int(config['app']['preview_width']),
                                                    int(config['app']['preview_height'])))
        sleep(2)
        camera.capture(path)
        camera.stop_preview()
    else:
        shutil.copyfile('sample.jpg',path)

def Preview(config):
    if CAMERA == 'pi':
       
        camera.start_preview(fullscreen=False,window=(int(config['app']['pvw_left_margin']),
                                                    int(config['app']['pvw_top_margin']),
                                                    int(config['app']['preview_width']),
                                                    int(config['app']['preview_height'])))
    
def Stop():
    if CAMERA == 'pi':
        camera.stop_preview()

