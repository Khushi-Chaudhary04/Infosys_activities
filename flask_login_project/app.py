from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Set up the database URI for SQLite (file-based database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid warning
app.secret_key = 'your_secret_key'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database
with app.app_context():
    db.create_all()  # Creates all the tables

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the user exists in the database
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:  # You should hash the password in a real application
        flash('Login Successful!', 'success')
        return redirect(url_for('welcome'))
    else:
        flash('Invalid username or password!', 'danger')
        return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    return 'Hello, you are logged in!'

if __name__ == '__main__':
    app.run(debug=True)
