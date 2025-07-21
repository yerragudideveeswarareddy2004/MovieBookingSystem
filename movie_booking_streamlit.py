import streamlit as st
import sqlite3

# Database setup (ensure this runs only once)
def get_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_tables():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        theatre TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        seats TEXT
    )''')
    conn.commit()
    conn.close()

create_tables()

st.title("Movie Booking System")

menu = ["Home", "Register", "Login", "Book Ticket"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.header("Welcome to the Movie Booking App!")
    # Show movies
    conn = get_db()
    movies = conn.execute('SELECT title, theatre FROM movies').fetchall()
    conn.close()
    if movies:
        for m in movies:
            st.write(f"**{m[0]}** at *{m[1]}*")
    else:
        st.info("No movies available.")

elif choice == "Register":
    st.header("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            st.success("Registration successful! Please log in.")
        except sqlite3.IntegrityError:
            st.error("Username or email already exists.")
        finally:
            conn.close()

elif choice == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        conn.close()
        if user:
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

elif choice == "Book Ticket":
    st.header("Book a Ticket")
    conn = get_db()
    movies = conn.execute('SELECT id, title FROM movies').fetchall()
    conn.close()
    if movies:
        movie_titles = [f"{m[1]} (ID: {m[0]})" for m in movies]
        selected = st.selectbox("Select Movie", movie_titles)
        seats = st.text_input("Seats (e.g. A1, A2)")
        if st.button("Book Now"):
            movie_id = int(selected.split('ID: ')[1][:-1])
            # For demo, user_id is set to 1
            conn = get_db()
            conn.execute('INSERT INTO bookings (user_id, movie_id, seats) VALUES (?, ?, ?)', (1, movie_id, seats))
            conn.commit()
            conn.close()
            st.success("Booking successful!")
    else:
        st.info("No movies available to book.") 