from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something more secure

# Initialize the SQLite database
import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')

    # Create the users table if it doesn't exist
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)')
    
    # Create the posts table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            condition TEXT,
            title TEXT,
            location TEXT,
            description TEXT,
            username TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

# Call the init_db function to initialize the database
init_db()



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize the error message
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cur.fetchone()
            
            if user and check_password_hash(user[3], password):  # Check if the password is correct
                session['user_id'] = user[0]  # Save user's ID in the session
                session['username'] = user[1]  # Save user's name in the session
                return redirect(url_for('home'))
            else:
                error = "Login Failed, please check your credentials"
    
    return render_template('login.html', error=error)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Hash the password for security

        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                        (username, email, hashed_password))
            conn.commit()

            # Automatically log in the user after signup
            user_id = cur.lastrowid
            session['user_id'] = user_id  # Save user's ID in the session
            session['username'] = username  # Save user's name in the session
            
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session to log the user out
    return redirect(url_for('home'))

# Additional routes for other pages

@app.route('/detail')
def detail():
    return render_template('detail.html')

#Signed in?
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        if 'user_id' in session:
            # Retrieve form data
            # Ensure we're getting the data directly from the form submitted by the user
            condition = request.form.get('condition')
            title = request.form.get('title')
            location = request.form.get('location')
            description = request.form.get('description')
            username = session.get('username')  # Get the username from the session

            # Debugging print statements to verify data
            print(f"Condition: {condition}, Title: {title}, Location: {location}, Description: {description}, Username: {username}")

            # Save to the database
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO posts (user_id, condition, title, location, description, username)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (session['user_id'], condition, title, location, description, username))
                conn.commit()

            # Redirect back to the posts page after submission
            return redirect(url_for('posts'))

    # Handle GET requests: Show the posts
    show_popup = 'user_id' not in session

    # Fetch posts from the database to display on the page
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT condition, title, location, description, username, date FROM posts ORDER BY date DESC")
        posts = cur.fetchall()

    return render_template('posts.html', show_popup=show_popup, posts=posts)


@app.route('/submit_post', methods=['POST'])
def submit_post():
    if 'user_id' in session:
        # Retrieve form data from the form with id 'comment-form'
        condition = request.form.get('condition')
        title = request.form.get('title')
        location = request.form.get('location')
        description = request.form.get('description')

        # Debugging print statements to verify data
        print(f"Condition: {condition}, Title: {title}, Location: {location}, Description: {description}")

        # Map the condition to the correct icon name
        icon_map = {
            'very_big_waves': 'tsunami',
            'great_conditions_for_surfing': 'surfing',
            'great_conditions_for_kite_and_windsurfing': 'kitesurfing',
            'bad_overall_conditions': 'sentiment_dissatisfied',
            'too_windy': 'air',
            'amazing_overall_conditions': 'local_fire_department'
        }
        icon_name = icon_map.get(condition, '')

        # Debugging print statement for the icon name
        print(f"Icon Name: {icon_name}")

        # Save to the database with the mapped icon name
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO posts (user_id, condition, title, location, description, username)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session['user_id'], icon_name, title, location, description, session['username']))
            conn.commit()

        # Redirect back to the posts page after submission
        return redirect(url_for('posts'))
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))





@app.route('/profile')
def profile():
    # You might want to protect this route so only logged-in users can access it
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
