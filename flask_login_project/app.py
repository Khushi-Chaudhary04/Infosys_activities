from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

# Initialize the Flask app
app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"  # Local MongoDB URI
mongo = PyMongo(app)

# Home route to show login form
@app.route('/')
def index():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Get username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists in database
        user = mongo.db.users.find_one({'username': username})
        
        if user:
            return f"Hello {username}, you are logged in!"
        else:
            # Store the user in the database
            mongo.db.users.insert_one({'username': username, 'password': password})
            return f"User {username} registered successfully!"
    
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
