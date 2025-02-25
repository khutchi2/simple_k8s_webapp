from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = '/app/data/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, title, content FROM messages ORDER BY id DESC')
    messages = cur.fetchall()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add_message():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO messages (title, content) VALUES (?, ?)',
                  [request.form['title'], request.form['content']])
        db.commit()
    return redirect(url_for('index'))

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=5000)
