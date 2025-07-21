import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Drop tables if they exist (for a clean setup)
c.execute('DROP TABLE IF EXISTS users')
c.execute('DROP TABLE IF EXISTS movies')
c.execute('DROP TABLE IF EXISTS bookings')

# Create users table with all required columns
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    phone TEXT,
    living TEXT
)
''')

# Create movies table (example schema)
c.execute('''
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    theatre TEXT NOT NULL,
    area TEXT NOT NULL,
    image_url TEXT
)
''')

# Create bookings table (example schema)
c.execute('''
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    seats TEXT,
    name TEXT,
    phone TEXT,
    email TEXT,
    cost INTEGER,
    date TEXT
)
''')

conn.commit()
conn.close()
print('Database and tables created!') 