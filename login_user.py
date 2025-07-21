import sqlite3

username = input("Enter your username: ")
password = input("Enter your password: ")

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
user = c.fetchone()
conn.close()

if user:
    print("Login successful!")
else:
    print("Invalid username or password.") 