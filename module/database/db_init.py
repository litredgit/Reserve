import sqlite3
import db

def db_path()  -> str:
    database_path = input(f"select a path for database reserve.db")
    return database_path
database_path = db_path()