# MikroKam
A Python application to manage a Raspberry Pi connected to a microscope.
Using the Raspberry Pi 7 inch touch screen, control the Raspberry Pi camera to capture images from a microscope.

# Getting Started
For this installation, it is assumed that you have a basic understanding of the Raspberry Pi and can download, install, and test an OS image, such as Raspbian.

## Prerequisites

### Hardware
* A Raspberry Pi. Developed on a Rpi 3, but tested on a Rpi 2.
  
* A Raspberry Pi 7" touchscreen. With some work, it will probably work on other displays.
  
* A Raspberry Pi camera. Only the CSI interface is supported. Any compatible camera should work.
  
* A network connection.

### Software
* Latest Raspbian image.
### Installation

Start with a fresh copy of Raspbian.

Start a terminal session.

cd to /home/pi

Unless you make some serious changes, MikroKam must exist in the /home/pi/MikroKam directory.
<code>
git clone https://github.com/greypanda/MikroKam.git
</code>
This will download MikroKam and create the MikroKam directory.
<code>
cd MikroKom
</code>
<code>
sudo cp MikroKom.desktop /home/pi/Desktop
</code>


You can start the program from the terminal by typing ./MikroKam or just double click the desktop icon.

You must have a formatted USB flash drive inserted to take snapshots.

You can also download a zip file, unzip it into /home/pi/MikroKom and follow the above directions.
