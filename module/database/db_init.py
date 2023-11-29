import os, json

def settings_init():
    _path = os.path.abspath(__file__)
    for i in range(3):
        _path = os.path.dirname(_path)
    db_path = {'db_path': os.path.join(_path, 'database', 'reserve.db').replace('\\', '/')}
    
    with open("settings.json", "w") as f:
        json.dump(db_path, f)
settings_init()
    
import db

with db.get_db() as initdb:
    initdb.create_table('users')
    print(f"create db")
    initdb.create_table('orbi23')
    initdb.add_column('users')
    initdb.add_column('orbi23')