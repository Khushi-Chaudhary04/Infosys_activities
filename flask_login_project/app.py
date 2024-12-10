from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for flash messages

# Connect to SQLite database (it will be created if it doesn't exist)
def get_db_connection():
    conn = sqlite3.connect('users.db')  # Database file
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Create table if not exists
def create_users_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            flash('Username already exists!', 'error')
            conn.close()
            return redirect(url_for('register'))
        
        # Insert new user into the database
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            flash(f'Hello, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

if __name__ == '__main__':
    create_users_table()  # Ensure the table is created when the app starts
    app.run(debug=True)
