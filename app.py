from flask import Flask, render_template, request, redirect, session, g
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'supersecret'
DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
       
        user_exists = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user_exists:
            return render_template('register.html', error="Користувач з таким ім’ям вже існує")
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/learn')
        else:
            return render_template('login.html', error="Невірні дані для входу")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/learn')
def learn():
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    word = db.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1").fetchone()
    return render_template('learn.html', word=word)

@app.route('/learned', methods=['POST'])
def learned():
    if 'user_id' not in session:
        return redirect('/login')
    word_id = request.form['word_id']
    user_id = session['user_id']
    db = get_db()
    
    exists = db.execute("SELECT * FROM learned WHERE user_id = ? AND word_id = ?", (user_id, word_id)).fetchone()
    if not exists:
        db.execute("INSERT INTO learned (user_id, word_id) VALUES (?, ?)", (user_id, word_id))
        db.commit()
    return redirect('/learn')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'user_id' not in session:
        return redirect('/login')

    
    if 'test_current' not in session:
        session['test_current'] = 0
        session['test_correct'] = 0

    if session['test_current'] >= 5:
        return redirect('/test_result')

    db = get_db()
    correct_word = db.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1").fetchone()
    options = [correct_word['ua']]

    while len(options) < 4:
        candidate = db.execute("SELECT ua FROM words ORDER BY RANDOM() LIMIT 1").fetchone()['ua']
        if candidate not in options:
            options.append(candidate)

    random.shuffle(options)

    return render_template('test.html', word=correct_word['en'], correct=correct_word['ua'], options=options)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    if 'user_id' not in session:
        return redirect('/login')

    selected = request.form['selected']
    correct = request.form['correct']
    result = selected == correct

    session['test_current'] = session.get('test_current', 0) + 1
    if result:
        session['test_correct'] = session.get('test_correct', 0) + 1

    return render_template('result.html', result=result, correct=correct)

@app.route('/test_result')
def test_result():
    total = session.get('test_current', 0)
    correct = session.get('test_correct', 0)

    session.pop('test_current', None)
    session.pop('test_correct', None)

    return render_template('final_result.html', total=total, correct=correct)


@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM learned WHERE user_id = ?", (user_id,)).fetchone()[0]
    return render_template('stats.html', count=count)

if __name__ == "__main__":
    app.run(debug=True)
