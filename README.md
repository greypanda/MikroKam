# MikroKam
A Python application to manage a Raspberry Pi connected to a microscope.
Using the Raspberry Pi 7 inch touch screen, control the Raspberry Pi camera to capture images from a microscope.

# Getting Started
For this installation, it is assumed that you have a basic understanding of the Raspberry Pi and can download, install, and test an OS image, such as Raspbian. You should also be comfortable with working in a terminal session using the command line.

## Prerequisites

### Hardware
* A Raspberry Pi. Developed on a Rpi 3, but tested on a Rpi 2.
  
* A Raspberry Pi 7" touchscreen. With some work, it will probably work on other displays.
  
* A Raspberry Pi camera. Only the CSI interface is supported. Any compatible camera should work.
  
* A network connection.
* A USB flashdrive for saving pictures.
* A USB keyboard and mouse (wireless is good)

### Software
* Latest Raspbian image.
### Installation

Start with a fresh copy of Raspbian.

Start a terminal session.

(If you can start a ssh session, it is easier to do this with a larger display!)

cd to /home/pi

Unless you make some serious changes, MikroKam must exist in the /home/pi/MikroKam directory.

<code>
git clone https://github.com/greypanda/MikroKam.git
</code>

This will download MikroKam and create the MikroKam directory.

<code>
cd MikroKam
</code>

Then to install or update the application:

<code>
  ./install
</code>

You can start the program from the terminal by typing ./MikroKam or just double click the desktop icon.

You must have a formatted USB flash drive inserted to take snapshots.

You can also download a zip file, unzip it into /home/pi/MikroKam and follow the above directions.

## Updates

With a working installation, you can update to the latest version by:

<code>
git pull
  
./install
</code>

This will save your current MikroKam.ini file as MikroKam.ini.save.

It also merges your current app settings into a new MikroKam.ini that has changes made to MikroKam.ini.dist.

## Operation
Operating the camera is very simple. There are only two functions needed to take a picture:
* Click the *Preview* button to show a live view of the camera image. This is used to focus the microscope or make other adjustments as necessary.
* Click the *Stop* button to end the preview. If the preview is left active for a period ( you can set this value ) it will automatically stop the preview.
* Click the *Snapshot* button to capture a photo of the image. You will be warned if the flash drive is not mounted or is not writable. 
* The name of the captured image file is displayed at the bottom of the screen.

To remove the flash drive, be sure to wait at least 10-15 seconds after the last snapshot to allow the data to be saved. It is always best to click the *eject* icon at the top right of the screen before removing the drive.

### Background and Future
This project has only been around since February 2018. The basic operations are working and there are enough controls to manage the generation of images. 

There is a large list of *potential* controls stored in the MikroKam.ini file. Only the section [app] is currently used. This is mostly to control the appearance of the screen. Eventually, there will be additional parameters that can be tweaked to manage the camera controls. We may even provide some on-screen tools to change commonly used controls.

### Features in the planning stage
* Saving of files on the local disk
* Network support ( web service? )
### Known Issues - in the queue

* The position of the application window is manually controlled and does not compensate for changes to the desktop.
* If a preview is active and the application is terminated, the preview stays on the screen. This can require a reboot of the system to correct.
