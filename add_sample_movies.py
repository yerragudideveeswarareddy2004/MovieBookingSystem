import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Clear existing movies (optional, for clean slate)
c.execute('DELETE FROM movies')

movies = [
    ('RRR', 'CineHub', 'Near Malli Golden Shop, Proddutur', '/static/RRR.jpg'),
    ('Jawan', 'PVR Max', 'Main Road, Kadapa', '/static/Jawan.jpg'),
    ('Leo', 'Cinepolis', 'Opp. RTC Bus Stand, Kurnool', '/static/Leo.jpg'),
    ('Pushpa 2', 'INOX Screen 2', 'Beside Reliance Mall, Tirupati', '/static/Pushpa2.jpg'),
    ('Salaar', 'Asian Cinemas', 'Near Gandhi Chowk, Anantapur', '/static/Salaar.jpg'),
]

c.executemany('INSERT INTO movies (title, theatre, area, image_url) VALUES (?, ?, ?, ?)', movies)
conn.commit()
conn.close()
print('Sample movies added!')

conn = sqlite3.connect('database.db')
for row in conn.execute('SELECT title, image_url FROM movies'):
    print(row)
conn.close() 