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

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Сторінка входу
@app.route('/')
def index():
    username = session.get('username')
    print(username)
    user_response = supabase.table('users').select('id').eq('username', username).execute()
    
    print(user_response.data[0]['id'])
    return '<h1>Text</h1>'


if __name__ == '__main__':
    app.run(debug=True)
