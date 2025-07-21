from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

DATABASE = 'database.db'

# Helper to get DB connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def home():
    conn = get_db()
    query = request.args.get('q', '').strip()
    if query:
        movies = conn.execute(
            "SELECT * FROM movies WHERE title LIKE ? OR theatre LIKE ? OR area LIKE ?",
            (f'%{query}%', f'%{query}%', f'%{query}%')
        ).fetchall()
    else:
        movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        print('Submitted:', username, password)
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        conn.close()
        print('User from DB:', user)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/receipt/<int:booking_id>')
def receipt(booking_id):
    conn = get_db()
    booking = conn.execute('SELECT * FROM bookings WHERE id=?', (booking_id,)).fetchone()
    movie = None
    if booking:
        movie = conn.execute('SELECT * FROM movies WHERE id=?', (booking['movie_id'],)).fetchone()
    conn.close()
    return render_template('receipt.html', booking=booking, movie=movie)

@app.route('/payment/<int:booking_id>')
def payment(booking_id):
    return render_template('payment.html', booking_id=booking_id)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    conn = get_db()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please log in to book tickets.', 'warning')
            return redirect(url_for('login'))
        movie_id = request.form['movie_id']
        seats = request.form['seats']
        user_id = session['user_id']
        cursor = conn.execute('INSERT INTO bookings (user_id, movie_id, seats) VALUES (?, ?, ?)', (user_id, movie_id, seats))
        booking_id = cursor.lastrowid
        conn.commit()
        flash('Booking successful!', 'success')
        conn.close()
        return redirect(url_for('payment', booking_id=booking_id))
    conn.close()
    return render_template('booking.html', movies=movies)

@app.route('/select_seats/<int:movie_id>', methods=['GET', 'POST'])
def select_seats(movie_id):
    conn = get_db()
    movie = conn.execute('SELECT * FROM movies WHERE id=?', (movie_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        seats = request.form['seats']
        cost = request.form['cost']
        date = request.form.get('date')
        # Store all booking details in bookings table
        cursor = conn.execute('INSERT INTO bookings (user_id, movie_id, seats, name, phone, email, cost, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (None, movie_id, seats, name, phone, email, cost, date))
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        flash('Booking successful! Thank you, {}.'.format(name), 'success')
        return redirect(url_for('payment', booking_id=booking_id))
    conn.close()
    return render_template('select_seats.html', movie=movie)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))
    conn = get_db()
    if request.method == 'POST':
        name = request.form.get('username')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        living = request.form.get('living')
        conn.execute('UPDATE users SET username=?, age=?, phone=?, email=?, living=? WHERE id=?',
                     (name, age, phone, email, living, session['user_id']))
        conn.commit()
        flash('Profile updated successfully!', 'success')
    user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/history')
def history():
    if 'user_id' not in session:
        flash('Please log in to view your booking history.', 'warning')
        return redirect(url_for('login'))
    conn = get_db()
    bookings = conn.execute('SELECT * FROM bookings WHERE user_id=? ORDER BY id DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('history.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 