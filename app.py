from flask import Flask, render_template, request, redirect, url_for
import sql_worker  # ваш модуль для работы с базой

app = Flask(__name__)

@app.route('/')
def index():
    # Главное меню или стартовая страница
    return render_template('index.html')

@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    # показать урок
    lesson_content = sql_worker.get_lesson_by_id(lesson_id)  # реализуйте в sql_worker
    return render_template('lesson.html', content=lesson_content)

@app.route('/test/<int:test_id>', methods=['GET', 'POST'])
def test(test_id):
    if request.method == 'POST':
        answer = request.form['answer']
        correct = sql_worker.check_answer(test_id, answer)
        return render_template('result.html', answer=answer, correct=correct)
    else:
        question = sql_worker.get_test_question(test_id)
        return render_template('test.html', question=question)

if __name__ == '__main__':
    app.run(debug=True)
