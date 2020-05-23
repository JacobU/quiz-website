function previousQuestion() {
    currentQuestion = document.getElementById("question-number");
    currentQuestion = currentQuestion + 1;
    document.getElementById("question-number").innerHTML = currentQuestion;
}

function nextQuestion() {
    currentQuestion = document.getElementById("question-number");
    currentQuestion = currentQuestion + 1;
    document.getElementById("question-number").innerHTML = currentQuestion;
}