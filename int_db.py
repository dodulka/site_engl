import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
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
    word_id INTEGER
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

conn.executemany("INSERT INTO words (en, ua) VALUES (?, ?)", words)
conn.commit()
conn.close()

print('Базу даних створено!')
