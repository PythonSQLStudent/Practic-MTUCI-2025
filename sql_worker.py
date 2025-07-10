"""Модуль для работы с БД"""
import sqlite3
import json
import os

DB_NAME = 'words.db'

def init_db_from_json():
    if os.path.exists(DB_NAME):
        return
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('CREATE TABLE words (en TEXT, ru TEXT, level TEXT)')
    with open('words.json', 'r', encoding='utf-8') as f:
        words = json.load(f)
        for w in words:
            level = w.get('level', 'easy')
            cur.execute('INSERT INTO words (en, ru, level) VALUES (?, ?, ?)', (w['en'], w['ru'], level))
    conn.commit()
    conn.close()

def init_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def init_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            user_id INTEGER,
            correct INTEGER,
            total INTEGER
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            total_correct INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def get_all_words():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT en, ru FROM words')
    rows = cur.fetchall()
    conn.close()
    return [{'en': r[0], 'ru': r[1]} for r in rows]

def get_words_by_level(level):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT en, ru FROM words WHERE level = ?', (level,))
    rows = cur.fetchall()
    conn.close()
    return [{'en': r[0], 'ru': r[1]} for r in rows]

def get_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        conn.close()
        return False
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True

def add_test_result(user_id, correct, total):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test_results (user_id INTEGER, correct INTEGER, total INTEGER)")
    cur.execute("INSERT INTO test_results (user_id, correct, total) VALUES (?, ?, ?)", (user_id, correct, total))
    conn.commit()
    conn.close()

def get_user_results(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT correct, total FROM test_results WHERE user_id = ?", (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def update_user_stats(user_id, correct):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
        user_id INTEGER PRIMARY KEY, total_correct INTEGER
    )''')
    cur.execute("SELECT total_correct FROM user_stats WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row:
        new_total = row[0] + correct
        cur.execute("UPDATE user_stats SET total_correct = ? WHERE user_id = ?", (new_total, user_id))
    else:
        cur.execute("INSERT INTO user_stats (user_id, total_correct) VALUES (?, ?)", (user_id, correct))
    conn.commit()
    conn.close()

def get_user_progress(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT total_correct FROM user_stats WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def get_words_by_level(level):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT en, ru FROM words WHERE level = ?', (level,))
    rows = cur.fetchall()
    conn.close()
    return [{'en': r[0], 'ru': r[1]} for r in rows]