import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.execute('PRAGMA table_info(users);')
for row in cursor:
    print(row)
conn.close() 