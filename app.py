from flask import Flask, render_template, request, redirect, url_for, current_app
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'todo.db'

def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
with app.app_context():
    init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
    todos = cursor.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE todos SET completed = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 