import os, json

def testprint():
    print("test done")
    
_path = os.path.abspath(__file__)
for i in range(3):
    _path = os.path.dirname(_path)
db_path = {'db_path': os.path.join(_path, 'database', 'reserve.db').replace('\\', '/')}

print(db_path)
with open("settings.json", "w") as f:
    #db_path = json.load(f)['db_path']
    json.dump(db_path, f)
    # print(json.load(f)['db_path'])