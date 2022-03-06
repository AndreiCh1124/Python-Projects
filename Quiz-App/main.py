from logic_models import Logic
from question_model import Question
from ui_models import Interface
from quiz_data import question_data
import html

from random import shuffle

question_number = len(question_data)

question_bank = list()
print(len(question_data))
for question in question_data:
    choices = list()
    question_text = html.unescape(question["question"])
    correct_answer = html.unescape(question["correct_answer"])
    incorrect_answer = question["incorrect_answers"]
    for answer in incorrect_answer:
        choices.append(html.unescape(answer))
    choices.append(correct_answer)
    shuffle(choices)
    new_question = Question(question_text, correct_answer, choices)
    question_bank.append(new_question)

quiz = Logic(question_bank)

quiz_ui = Interface(quiz)

print("You have completed the quiz !!!")
print(f"Your final score is : {quiz.score}/{quiz.question_no}")