"""Installation

    * Are the files all here?
    * do the md5s match the calculated values

    Then:

    rename "this" file
    copy the main python file to a none .py file.

    save the old .ini file

    copy the dist .ini file to .ini

    restore the photo numbers

    run the new file
"""

import sys,hashlib
import configparser
import os.path
import shutil
import stat
import subprocess

CURRENT_INI = 'MikroKam.ini'
OLD_INI = 'MikroKam.ini.old'
DIST_INI = 'MikroKam.ini.dist'
CURRENT_VERSION = '0.2.1'
DIST_VERSION = '0.2.2'

INSTALL_TYPE = 'update'



def getmd5(fname):


    hash_md5 = hashlib.md5()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        print("failed open file: %s" % fname)
        return None




print("Welcome to MikroKam")
if sys.version_info[0] < 3:
    print("Python version 3 is required -- found %s" % sys.version_info[0])
    sys.exit(1)
os.system('pip3 install pyudev')
os.system('pip3 install Pillow')
os.system('pip3 install psutil')


print("Installing version %s" % DIST_VERSION)
print("Replacing  version %s" % CURRENT_VERSION)
print("------------------------------------------")
print("Checking MD5 checksums for critical files")
with open('mikrokam.md5','r') as infile:
    content = infile.readlines()
for line in content:
    f,m = line.split(":")
    m = m.strip()
    a = getmd5(f)
    if a != m:
        print("Installation failed. Checksums do not match for %s" % f)
        sys.exit()
    else:
        print("==>%s matches" % f)
print("Checksums match")
print("------------------------------------------")
print("Processing configuration files")
# if there is no current ini file, assume a new install
if not os.path.isfile(CURRENT_INI):
    print("Can't find current ini file: %s" % CURRENT_INI)
    print("Assuming this is a new installation")
    INSTALL_TYPE = 'new'
    current_config = configparser.ConfigParser()
else:
    print("Reading current config file")
    current_config = configparser.ConfigParser()
    current_config.read(CURRENT_INI)
    try:
        current_version = current_config['software']['version']   
    except KeyError:
        print("Current ini (%s)  appears to be invalid" % CURRENT_INI)
        print("File has no version")
        sys.exit()

# save the current config as old
print("Save the current configuration file %s as %s" % (CURRENT_INI,OLD_INI))
with open(OLD_INI,'w') as configfile:
    current_config.write(configfile)

## see if the distribution ini has the version
print("Check that the distribution config file has versioin")
dist_config = configparser.ConfigParser()
dist_config.read(DIST_INI)
try: 
    new_version = dist_config['software']['version']
except KeyError:
    print(" file is invalid, no version number")
    print("Installation aborted")



if INSTALL_TYPE == 'update':
    print("Updating the new configuration with current configuration")
    # get the old app data
    current_app = list(current_config.items('app'))
    for parm in current_app:
        key,value = parm
        dist_config['app'][key] = value



print("Copy the new file %s to the current %s" % (DIST_INI,CURRENT_INI))
# "copy" the new ini to the current
with open(CURRENT_INI,'w') as cfile:
    dist_config.write(cfile)

print("Creating executable application file")
shutil.copyfile('MikroKam.py','MikroKam')
st = os.stat('MikroKam')

os.chmod('MikroKam',st.st_mode | stat.S_IEXEC)
print("moving install.py to install.py.used")
os.rename('install.py','install.py.used')

subprocess.Popen(['./MikroKam'])
sys.exit(0)
