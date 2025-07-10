from flask import Flask, render_template, request, redirect, jsonify, session
import random
from sql_worker import *

app = Flask(__name__)
app.secret_key = 'super_secret_key'

init_db_from_json()
init_users()
init_stats()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lesson')
def lesson():
    return render_template('lesson.html')

@app.route('/test')
def choose_level():
    return render_template('test_level.html')

@app.route('/test/<level>')
def test(level):
    if level not in ['easy', 'medium', 'hard']:
        return "Недопустимый уровень", 400
    return render_template('test.html', level=level)

@app.route('/api/new_word')
def new_word():
    return jsonify(random.choice(get_all_words()))

@app.route('/api/exercise_word')
def exercise_word():
    word = random.choice(get_all_words())
    shuffled = list(word['en'])
    random.shuffle(shuffled)
    return jsonify({'en': word['en'], 'ru': word['ru'], 'shuffled': ''.join(shuffled)})

@app.route('/api/test_question/<level>')
def test_question(level):
    words = get_words_by_level(level)
    if not words:
        return jsonify({'error': 'Нет слов'}), 400
    correct = random.choice(words)
    options = [correct['ru']]
    wrongs = [w['ru'] for w in words if w != correct]
    options += random.sample(wrongs, min(3, len(wrongs)))
    random.shuffle(options)
    return jsonify({'en': correct['en'], 'options': options})

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    words = get_all_words()
    correct = next((w for w in words if w['en'] == data['en']), None)
    if correct and correct['ru'] == data['answer']:
        return jsonify({'result': 'correct'})
    return jsonify({'result': 'wrong', 'correct': correct['ru']})

@app.route('/test_result')
def test_result():
    score = int(request.args.get('score', 0))
    total = int(request.args.get('total', 5))
    message = "Отлично! 👍" if score >= total // 2 else "Попробуй снова! 👎"
    user_id = session.get('user_id')
    if user_id:
        add_test_result(user_id, score, total)
        update_user_stats(user_id, score)
    return render_template('test_result.html', score=score, total=total, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = get_user(request.form['username'], request.form['password'])
        if user:
            session['user_id'] = user[0]
            session['username'] = request.form['username']
            return redirect('/')
        error = 'Неверные данные'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        success = create_user(request.form['username'], request.form['password'])
        if success:
            return redirect('/login')
        error = 'Пользователь уже существует'
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dictionary')
def dictionary():
    return render_template('dictionary.html', words=get_all_words())

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('history.html', results=get_user_results(session['user_id']), username=session['username'])

@app.route('/progress')
def progress():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('progress.html', correct=get_user_progress(session['user_id']), username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
