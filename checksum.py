"""Check maker

    creates a file with a list of checksums for downloaded files

    Not all files are checked

"""
import sys,hashlib

files = ['autoupdate.py',
        'flashman.py',
        'mainpage.py',
        'MikroKam.ini.dist',
        'MikroKam.py',
        'requirements.txt',
    
        ]

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

fd = open('mikrokam.md5','w')
for i in files:
    a = getmd5(i)

    if a:
        fd.write(i + ':' + a + "\n" )
  
fd.close()