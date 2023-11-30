import os, json, sqlite3

def setcwd():
    cwdpath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwdpath)
    return cwdpath
cwdpath = setcwd()