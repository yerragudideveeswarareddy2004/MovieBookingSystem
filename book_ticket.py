import sqlite3

username = input("Enter your username: ")
movie_title = input("Enter the movie title: ")
seats = int(input("Enter number of seats: "))

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Get user ID
c.execute("SELECT id FROM users WHERE username=?", (username,))
user = c.fetchone()
if not user:
    print("User not found.")
    conn.close()
    exit()
user_id = user[0]

# Get movie ID
c.execute("SELECT id FROM movies WHERE title=?", (movie_title,))
movie = c.fetchone()
if not movie:
    print("Movie not found.")
    conn.close()
    exit()
movie_id = movie[0]

# Insert booking
c.execute("INSERT INTO bookings (user_id, movie_id, seats) VALUES (?, ?, ?)", (user_id, movie_id, seats))
conn.commit()
conn.close()
print("Booking successful!") 