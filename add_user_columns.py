import sqlite3
conn = sqlite3.connect('database.db')
try:
    conn.execute('ALTER TABLE users ADD COLUMN age INTEGER;')
except Exception as e:
    print(e)
try:
    conn.execute('ALTER TABLE users ADD COLUMN phone TEXT;')
except Exception as e:
    print(e)
try:
    conn.execute('ALTER TABLE users ADD COLUMN living TEXT;')
except Exception as e:
    print(e)
conn.commit()
conn.close()
print('Columns added (or already exist).') 