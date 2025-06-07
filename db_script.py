import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    en TEXT,
    ua TEXT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS learned (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    word_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(word_id) REFERENCES words(id)
)
''')


words = [
    ('apple', 'яблуко'),
    ('dog', 'пес'),
    ('milk', 'молоко'),
    ('sun', 'сонце'),
    ('car', 'машина'),
    ('house', 'будинок'),
    ('book', 'книга'),
    ('water', 'вода'),
    ('fire', 'вогонь'),
    ('sky', 'небо')
]


for en, ua in words:
    conn.execute("INSERT OR IGNORE INTO words (en, ua) VALUES (?, ?)", (en, ua))

conn.commit()
conn.close()

print('Базу даних створено і заповнено!')
