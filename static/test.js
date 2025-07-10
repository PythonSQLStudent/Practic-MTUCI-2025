let currentEn = '';
let score = 0;
let questionIndex = 0;
const totalQuestions = 5;

function loadTest() {
    if (questionIndex >= totalQuestions) {
        window.location.href = `/test_result?score=${score}&total=${totalQuestions}`;
        return;
    }

    fetch(`/api/test_question/${testLevel}`)
        .then(res => res.json())
        .then(data => {
            currentEn = data.en;
            let html = `<p><b>Вопрос ${questionIndex + 1}:</b> Что значит "<strong>${data.en}</strong>"?</p>`;
            html += '<div id="options">';
            data.options.forEach(opt => {
                html += `<button onclick="submitAnswer(this, '${opt}')">${opt}</button><br>`;
            });
            html += '</div>';
            document.getElementById('question-area').innerHTML = html;
            document.getElementById('feedback').innerText = '';
        });
}

function submitAnswer(button, answer) {
    // Отключаем все кнопки
    document.querySelectorAll('#options button').forEach(btn => btn.disabled = true);

    fetch('/api/check_answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ answer: answer, en: currentEn })
    })
    .then(res => res.json())
    .then(data => {
        let isCorrect = data.result === 'correct';
        if (isCorrect) score++;
        document.getElementById('feedback').innerText =
            isCorrect ? '✅ Верно!' : `❌ Неверно. Правильный ответ: ${data.correct}`;
        
        questionIndex++;
        setTimeout(loadTest, 1500);
    });
}

window.onload = loadTest;
