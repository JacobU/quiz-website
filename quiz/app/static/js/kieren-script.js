window.onload = startCount();

function startCount() {
    window.answersCorrect = 0;
    document.getElementById("count").innerHTML = parseInt(window.answersCorrect);

    window.recordedAnswers = [];
}

function increment() {
    window.answersCorrect = parseInt(window.answersCorrect) + 1;
    document.getElementById("count").innerHTML = parseInt(window.answersCorrect);
}

$(function(){

    $(document).on("click",".option", function (){
        currentQuestion = parseInt(document.getElementById("question-number").innerHTML);
        
        console.log($(this).html())
        window.recordedAnswers.push($(this).html());
        switch(currentQuestion) {
            case 1:
                if( "{{ corrAnswers[0] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 2:
            if( "{{ corrAnswers[1] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 3:
            if( "{{ corrAnswers[2] }}" ==  $(this).html()) {
                    increment();
                } 
                break;
            case 4:
                if( "{{ corrAnswers[3] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 5:
                if( "{{ corrAnswers[4] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 6:
                if( "{{ corrAnswers[5] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 7:
                if( "{{ corrAnswers[6] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 8:
                if( "{{ corrAnswers[7] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 9:
                if( "{{ corrAnswers[8] }}" ==  $(this).html()) {
                    increment();
                }
                break;
            case 10:
                if( "{{ corrAnswers[9] }}" ==  $(this).html()) {
                    increment();
                }
                break;
        }
        nextQuestion();
    });


}); 

function nextQuestion() {

    currentQuestion = parseInt(document.getElementById("question-number").innerHTML);
    if(currentQuestion < 10) {
        currentQuestion = currentQuestion + 1;
        document.getElementById("question-number").innerHTML = currentQuestion;
        

        // OK yes, I know this is a massive HACK but all the other ways were fucking me up
        switch(currentQuestion) {
            case 1:
                document.getElementById("question").innerHTML = "{{ questions[0] }}";
                document.getElementById("one").innerHTML = "{{ answers[0][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[0][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[0][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[0][3] }}";
                break;
            case 2:
                document.getElementById("question").innerHTML = "{{ questions[1] }}";
                document.getElementById("one").innerHTML = "{{ answers[1][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[1][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[1][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[1][3] }}";
                break;
            case 3:
                document.getElementById("question").innerHTML = "{{ questions[2] }}";
                document.getElementById("one").innerHTML = "{{ answers[2][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[2][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[2][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[2][3] }}";
                break;
            case 4:
                document.getElementById("question").innerHTML = "{{ questions[3] }}";
                document.getElementById("one").innerHTML = "{{ answers[3][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[3][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[3][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[3][3] }}";
                break;
            case 5:
                document.getElementById("question").innerHTML = "{{ questions[4] }}";
                document.getElementById("one").innerHTML = "{{ answers[4][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[4][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[4][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[4][3] }}";
                break;
            case 6:
                document.getElementById("question").innerHTML = "{{ questions[5] }}";
                document.getElementById("one").innerHTML = "{{ answers[5][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[5][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[5][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[5][3] }}";
                break;
            case 7:
                document.getElementById("question").innerHTML = "{{ questions[6] }}";
                document.getElementById("one").innerHTML = "{{ answers[6][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[6][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[6][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[6][3] }}";
                break;
            case 8:
                document.getElementById("question").innerHTML = "{{ questions[7] }}";
                document.getElementById("one").innerHTML = "{{ answers[7][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[7][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[7][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[7][3] }}";
                break;
            case 9:
                document.getElementById("question").innerHTML = "{{ questions[8] }}";
                document.getElementById("one").innerHTML = "{{ answers[8][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[8][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[8][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[8][3] }}";
                break;
            case 10:
                document.getElementById("question").innerHTML = "{{ questions[9] }}";
                document.getElementById("one").innerHTML = "{{ answers[9][0] }}";
                document.getElementById("two").innerHTML = "{{ answers[9][1] }}";
                document.getElementById("three").innerHTML = "{{ answers[9][2] }}";
                document.getElementById("four").innerHTML = "{{ answers[9][3] }}";
                break;
        }
        document.getElementById("displayAnswers").innerHTML = window.recordedAnswers.toString();
    }
}