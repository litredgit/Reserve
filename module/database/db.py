import sqlite3
from flask import Flask, request, jsonify
import db_init

class get_db:
    def __init__(self) -> str:
        pass

    def __enter__(self):
        self.conn = sqlite3.connect(db_init.database_path)
        self.cursor = self.conn.cursor()
        print("connect db")
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
        print("close db")
    
    def exec(self, command:str, list:list):
        self.cursor.execute(command, list)
        self.conn.commit()
        
    def execm(self, command:str, list:list):
        self.cursor.executemany(command, list)
        self.conn.commit()
    
    def insert(self, rownames: list, table_name, column):
        statement = f"INSERT INTO {table_name} ({column}) VALUES (?)"
        self.execm(statement, rownames)
            
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
            self.conn.commit()
            
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


#with get_db() as test:
    #test.insert(user_name, 'users', 'name')
    #test.insert(date, 'orbi', 'date')
    #test.reserve(request_info)