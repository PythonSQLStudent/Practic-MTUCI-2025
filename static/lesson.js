let currentWord = '';

function loadWord() {
    fetch('/api/new_word')
        .then(res => res.json())
        .then(data => {
            document.getElementById('word-area').innerText = `${data.en} — ${data.ru}`;
        });

    fetch('/api/exercise_word')
        .then(res => res.json())
        .then(data => {
            currentWord = data.en;
            document.getElementById('exercise-area').innerText = `Перевод: ${data.ru} \nСлово (перемешано): ${data.shuffled}`;
            document.getElementById('result').innerText = '';
            document.getElementById('guess').value = '';
        });
}

function checkGuess() {
    const userInput = document.getElementById('guess').value.trim().toLowerCase();
    const correct = currentWord.toLowerCase();
    if (userInput === correct) {
        document.getElementById('result').innerText = '✅ Правильно!';
    } else {
        document.getElementById('result').innerText = `❌ Неправильно. Верно: ${currentWord}`;
    }
}

window.onload = loadWord;
