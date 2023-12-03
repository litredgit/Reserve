import os, json, sqlite3

def setcwd():
    cwdpath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwdpath)
    return cwdpath

cwdpath = setcwd()

def set_db_path():
    """set db_path into settings.json"""
    with open('settings.json', 'w') as f:
        db_path = {'db_path': os.path.join(cwdpath, 'database', 'reserve.db').replace('\\', '/')}
        json.dump(db_path, f)