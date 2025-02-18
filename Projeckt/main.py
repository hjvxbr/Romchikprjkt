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

        if response.error:
            flash('Помилка під час реєстрації!')
        else:
            flash('Реєстрація успішна!')

        return redirect(url_for('index'))
    return render_template('register.html')

# Submit complaint logic
@app.route('/submit_complaint', methods=['POST', 'GET'])
def submit_complaint():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    user_response = supabase.table('users').select('id').eq('username', session['username']).execute()
    user_id = user_response.data[0]['id']
    print('ID =<', user_id)

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

# Логін роботодавця
@app.route('/employer-login', methods=['POST'])
def redrect_employer():
    return redirect(url_for('employer_login'))

@app.route('/employer-login')
def employer_login():
    return render_template('employer_login.html')

# Login logic for employers
@app.route('/employere', methods=['POST'])
def login_employer():
    user_name = request.form['username']
    password = request.form['password']
    company = request.form['company']
    
    # Check employer in the Supabase table 'robota'
    employer_response = (
        supabase.table('robota')
        .select('*')
        .eq('user_name', user_name)
        .execute()
    )
    print(employer_response)
    if employer_response.data and len(employer_response.data) > 0:
        session['employer_username'] = user_name
        flash('Вхід успішний!')
        return redirect(url_for('page'))
    else:
        flash('Невірні облікові дані або компанія не знайдена!')
        return redirect(url_for('employer_login'))

if __name__ == '__main__':
    app.run(debug=True)
