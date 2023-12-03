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
    
    def create_table(self, table:str):
        statement =f'''CREATE TABLE IF NOT EXISTS {table}
                  (id INTEGER PRIMARY KEY)'''
        self.exec(statement)
        print(f"create db.table: {table}")
    
    def conv_list(self, list:list, user_name:str="") -> list:
        """convert list into the format[(value,), ...] for sqlite3"""
        if user_name == "":
            list = [(x,) for x in list]
        else:
            list = [(user_name, x) for x in list]
        return list
        
    def add_column(self, table:str, column:list):
        print(f"add column: {column[0]} to {column[-1]} into table: {table}")
        for name in column:
            statement = f"ALTER TABLE {table} ADD COLUMN {name} TEXT;"
            self.exec(statement)
        
    def insert_row(self, table:str, column:str, rows:list):
        print(f"insert {rows[0]} to {rows[-1]} into table: {table}")
        rows = self.conv_list(rows)
        statement = f"INSERT INTO {table} ({column}) VALUES (?)"
        self.execm(statement, rows)
            
    def check(self, table:str, date:str='') -> dict:
        if table == 'users':
            statement = f"SELECT id, name FROM {table}"
        else:
            statement = f"SELECT time, {date} FROM {table}"
        self.exec(statement)
        rows = self.cursor.fetchall()
        output = {}
        for row in rows:
            output[row[0]] = row[1]
        return output
        
    def reserve(self, user:str, table:str, date:str, rt:list):
        rt = self.conv_list(rt, user)
        statement = f"UPDATE {table} SET {date} = ? WHERE time = ?"
        self.execm(statement, rt)
        print(f"reserve done")    

class maintain(get_db):
    def __init__(self) -> str:
        pass
        
    def set_time(self) -> list:
        """generate time_list for reservable time frame in a day"""
        rows = ['before9']
        for i in range(9,21):
            j = i + 1
            rows.append(f't{i}_{j}')
        rows.append('after21')
        return rows
    
    def set_date(self, year:int) -> list:
        """generate date_list in a year"""
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
        self.insert_row(instru_name, 'time', self.set_time())