import sqlite3, json, calendar

def get_settings() -> str:
    with open("settings.json", "r") as f:
        settings = json.load(f)
    return settings
db_path = get_settings()['db_path']

class get_db:
    def __init__(self) -> str:
        pass
    
    def __enter__(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        print("connect db")
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
        print("close db")
    
    def exec(self, command:str, list:list = []):
        self.cursor.execute(command, list)
        self.conn.commit()
        
    def execm(self, command:str, list:list = []):
        self.cursor.executemany(command, list)
        self.conn.commit()
    
    def create_table(self, table_name:str):
        statement =f'''CREATE TABLE IF NOT EXISTS {table_name}
                  (id INTEGER PRIMARY KEY)'''
        self.exec(statement)
        print(f"create db.table: {table_name}")
    
    def conv_list(self, list:list, user_name:str="") -> list:
        if user_name == "":
            list = [(x,) for x in list]
        else:
            list = [(user_name, x) for x in list]
        return list
        
    def add_column(self, table_name:str, column_name:list):
        print(f"add column: {column_name[0]} to {column_name[-1]} into table: {table_name}")
        for name in column_name:
            statement = f"ALTER TABLE {table_name} ADD COLUMN {name} TEXT;"
            self.exec(statement)
        
    def insert_row(self, rows: list, table_name, column):
        print(f"insert {rows[0]} to {rows[-1]} into table: {table_name}")
        rows = self.conv_list(rows)
        statement = f"INSERT INTO {table_name} ({column}) VALUES (?)"
        self.execm(statement, rows)
            
    def check_available(self, request_info:dict) -> dict:
        statement = f"SELECT time, {request_info['date']} FROM {request_info['table']}"
        self.exec(statement)
        rows = self.cursor.fetchall()
        output = {}
        for row in rows:
            output[row[0]] = row[1]
        return output
        
    def reserve(self, request_info:dict) -> dict:
        rt = self.conv_list(request_info['rt'], request_info['user'])
        statement = f"UPDATE {request_info['table']} SET {request_info['date']} = ? WHERE time = ?"
        self.execm(statement, rt)
        print(f"reserve done")    

class maintain(get_db):
    def __init__(self) -> str:
        pass
        
    def set_time(self) -> list:
        rows = ['before9']
        for i in range(9,21):
            j = i + 1
            rows.append(f't{i}_{j}')
        rows.append('after21')
        return rows
    
    def set_date(self, year:int) -> list:
        calendar.setfirstweekday(calendar.MONDAY)
        days = [calendar.monthrange(year, month)[1] for month in range(1, 13)]
        dates = [f"{calendar.month_abbr[month]}{str(day).zfill(2)}" for month, days in enumerate(days, start=1) for day in range(1, days+1)]
        return dates
    
    def user_table(self):
        self.create_table('users')
        self.add_column('users', ['name'])
        
    def instru_table(self, instru_name:str, year:int):
        self.create_table(instru_name)
        self.add_column(instru_name, ['time']+self.set_date(year))
        self.insert_row(self.set_time(), instru_name, 'time')