import db

with db.get_db() as initdb:
    initdb.create_table('users')
    print(f"create db")
    initdb.create_table('orbi23')
    initdb.add_column('users')
    initdb.add_column('orbi23')