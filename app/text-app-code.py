# app.py
from flask import Flask, request, render_template, redirect, url_for
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS text_entries (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# In Flask 3.0.0, before_first_request is removed, so we use a different approach
# Initialize database when app starts
@app.route('/init-db', methods=['GET'])
def initialize_db():
    init_db()
    return "Database initialized successfully"

# Call this function in a startup script or from your Kubernetes init container
# Alternatively, you can use Flask's cli commands or built-in callbacks in the app factory pattern

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, content, created_at FROM text_entries ORDER BY created_at DESC')
    entries = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    content = request.form['content']
    if content:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO text_entries (content) VALUES (%s)', (content,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Make sure the database is initialized at startup
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=8080)