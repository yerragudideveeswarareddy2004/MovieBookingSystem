import sqlite3

conn = sqlite3.connect('database.db')
try:
    conn.execute('ALTER TABLE bookings ADD COLUMN date TEXT;')
    print('Date column added!')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Date column already exists.')
    else:
        print('Error:', e)
finally:
    conn.commit()
    conn.close()

conn = sqlite3.connect('database.db')
cursor = conn.execute('PRAGMA table_info(bookings);')
for row in cursor:
    print(row)
conn.close() 