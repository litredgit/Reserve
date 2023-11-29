import os, json

def testprint():
    print("test done")
    
_path = os.path.abspath(__file__)
for i in range(3):
    _path = os.path.dirname(_path)
settings_path = os.path.join(_path, 'database', 'settings.json')

with open(settings_path, 'r') as f:
    db_path = json.load(f)['db_path']
    
print(db_path)