"""Flash Drive Manager

    Update software from Flash

    Set up destination for snapshots 

    Detect mount/unmount

    version 0.2.1
"""
import pyudev
import psutil
import tempfile

class FlashMan():

    def __init__(self,master):
        self.master=master
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by('block')
        self.observer = pyudev.MonitorObserver(self.monitor,self.log_event)
        self.observer.start()
        pass

    def log_event(self,action,device):
            #messagebox.showerror('error','mounted')
            self.master.event_generate("<<myevent>>",when="tail",data="my data")  

    def usblist(self):
        """Detect and report on available USB drives"""

        ulist = []
        removable = [device for device in self.context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
        for device in removable:
            partitions = [device.device_node for device in self.context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            for p in psutil.disk_partitions():
                if p.device in partitions:
                    ulist.append(p.mountpoint)
        return ulist

    def isWritable(self,path):
        """Test to see if the usb drive can be written"""
        try:
            testfile = tempfile.TemporaryFile(dir = path)
            testfile.close()
        except OSError as e:
            return False
        return True
