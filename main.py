from flask import Flask, render_template, request, redirect, url_for, flash, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY  # Use the Flask secret key from the environment

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Home page with login
@app.route('/')
def index():
    if 'username' in session:  # Check if the user is already logged in
        return redirect(url_for('page'))
    return render_template('login.html')

# Login logic
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user_response = supabase.table('users').select('*').eq('username', username).execute()

    if user_response.data and len(user_response.data) > 0:
        user = user_response.data[0]
        if user['password'] == password:
            session['username'] = username  # Store user in session
            print("Успішно зайдено")  # Вивід у консоль
            return redirect(url_for('page'))
        else:
            flash('Невірний логін або пароль!')
    else:
        flash('Користувач не знайдений!')
    
    return redirect(url_for('index'))

# Registration logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['newUsername']
        password = request.form['newPassword']
        
        response = supabase.table('users').insert({"username": username, "password": password}).execute()

        return redirect(url_for('index'))
    return render_template('register.html')

# Submit complaint logic
@app.route('/submit_complaint', methods=['POST', 'GET'])
def submit_complaint():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    user_response = supabase.table('users').select('id').eq('username', session['username']).execute()
    user_id = user_response.data[0]['id']
    print('ID =', user_id)

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        resume_text = request.form['resume']

        supabase.table('applications').insert({
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "resume": resume_text,
            "user_id": user_id
        }).execute()

        flash('Заявка успішно відправлена!')
        return redirect(url_for('thank_you'))


    return render_template('submit_complaint.html')

# Thank you page
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Logged-in page
@app.route('/page')
def page():
    if 'username' in session:
        return render_template('page.html', username=session['username'])
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('index'))

@app.route('/employer')
def employer_login():
    return render_template('employer_login.html')

@app.route('/employer-successful')
def success_employer_login():
    # Query Supabase to get the data from the 'applications' table
    response = supabase.table('applications').select('*').execute()

    # Check if data is retrieved successfully
    applications_data = response.data if response.data else []

    # Pass the data to the template
    return render_template('robota.html', applications_data=applications_data)

# Login logic
@app.route('/employere', methods=['POST'])
def login_employer():
    username = request.form.get('username')  # Use .get() to avoid KeyError
    password = request.form.get('password')
    company = request.form.get('company')

    if not username or not password or not company:
        flash("Missing fields!")  # Flash a message if any field is missing
        return redirect(url_for('employer_login'))

    # Query Supabase to check if user exists
    response = supabase.table('robota').select('*').eq('user_name', username).eq('company', company).execute()
    # Check if the user exists and password matches
    if response.data:
        user_data = response.data[0]
        if user_data['password'] == password:
            print(f"Login successful for user: {username}")
            return redirect(url_for('success_employer_login'))
        else:
            print("Incorrect password")
            flash("Incorrect password!")
    else:
        print(f"User {username} not found or company mismatch")
        flash("User not found or company mismatch!")

    return redirect(url_for('employer_login'))

if __name__ == '__main__':
    app.run(debug=True)

