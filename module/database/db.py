import sqlite3
import settings

class get_db:
    def __init__(self) -> str:
        self.elist = [0]

    def __enter__(self):
        self.conn = sqlite3.connect(settings.db_path)
        self.cursor = self.conn.cursor()
        print("connect db")
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
        print("close db")
    
    def exec(self, command:str, list:list):
        if list == self.elist:
            self.cursor.execute(command)
            self.conn.commit()
        else:
            self.cursor.execute(command, list)
            self.conn.commit()
        
    def execm(self, command:str, list:list):
        if list == self.elist:
            self.cursor.executemany(command)
            self.conn.commit()
        else:
            self.cursor.executemany(command, list)
            self.conn.commit()
    
    def create_table(self, table_name: str):
        statement =f'''CREATE TABLE IF NOT EXISTS {table_name}
                  (id INTEGER PRIMARY KEY)'''
        self.exec(statement, self.elist)
        print(f"create db.table: {table_name}")
    
    def set_time(self) -> list:
        column_name = ['date', 'before9']
        for i in range(9,21):
            j = i + 1
            column_name.append(f't{i}_{j}')
        column_name.append('after21')
        return column_name
        
    def add_column(self, table_name:str):
        column_name =self.set_time()
        if table_name == 'users':
            statement = f"ALTER TABLE {table_name} ADD COLUMN 'name' TEXT;"
            self.exec(statement, self.elist)
        else:
            for name in column_name:
                statement = f"ALTER TABLE {table_name} ADD COLUMN {name} TEXT;"
                self.exec(statement, self.elist)
        print(f"add column")
        
    def insert(self, rownames: list, table_name, column):
        statement = f"INSERT INTO {table_name} ({column}) VALUES (?)"
        self.execm(statement, rownames)
        print(f"insert {rownames[0]} to {rownames[-1]}")
            
    def check_available(self, request_info:dict) -> dict:
        check_info = [(request_info['table'], request_info['date'])]
        statement = f"SELECT * FROM ? WHERE 'date' = ?"
        self.exec(statement, check_info)
        rows = self.cursor.fetchall()
        output = []
        for row in rows:
            print(row)
            
        return self
        
    def reserve(self, request_info:dict) -> dict:
        for key in request_info['rt']:
            reserve_info = [request_info['user'], request_info['date']]
            statement = f"UPDATE {request_info['table']} SET {request_info['rt'][key]} = ? WHERE date = ?"
            self.exec(statement, reserve_info)
        print(f"reserve done")    
        
request_info = {
            'user': 'pxy',
            'table': 'orbi',
            'date': 231128,
            'ct':{'t1':'t9_10',
                   't2':'t10_11',
                   },
            'rt': {'t1':'t9_10',
                   't2':'t10_11',
                   }
        }
user_name = [('crs',)]
date = [(231128,)]


with get_db() as test:
    #test.insert(user_name, 'users', 'name')
    #test.insert(date, 'orbi', 'date')
    #test.reserve(request_info)
    #test.create_table('orbi')
    pass