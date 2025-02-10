from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = '1234'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'bookmyshow'  # Name of your database

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Store user data in the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        
        flash('Signed up successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check user credentials
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]  # Store user ID in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('movies'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/movies')
def movies():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, title, genre, release_date FROM movies")  # Ensure this table exists in your database
    movies_list = cursor.fetchall()
    cursor.close()
    return render_template('movies.html', movies=movies_list)


if __name__ == '__main__':
    app.run(debug=True)
