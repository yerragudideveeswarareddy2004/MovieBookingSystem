import sqlite3
from send_otp import send_otp

email = input("Enter your email: ")
otp = send_otp(email)
user_otp = input("Enter the OTP sent to your email: ")

if user_otp == otp:
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username or email already exists.")
    conn.close()
else:
    print("Invalid OTP.") 