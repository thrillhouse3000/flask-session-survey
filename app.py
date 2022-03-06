from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secretsecret'
debug = DebugToolbarExtension(app)

survey = surveys.satisfaction_survey
responses = []

@app.route('/')
def home_page():
    title = survey.title
    instructions = survey.instructions
    return render_template('home.html', title=title, instructions=instructions) 

@app.route('/thanks')
def thanks_page():
    return render_template('thanks-page.html')


@app.route('/questions/<int:num>')
def show_questions(num):
    if len(responses) < num or num < len(responses):
        flash('Invalid URL', 'error')
        return redirect(f'/questions/{len(responses)}')
    elif len(responses) == len(survey.questions):
        return redirect('/thanks')
    else:
        question = survey.questions[num].question
        choices = survey.questions[num].choices
        return render_template('question-page.html', question=question, choices=choices, num=num)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['choice']
    responses.append(answer)
    if len(survey.questions) == len(responses):
        return redirect('/thanks')
    else:
        return redirect(f'/questions/{len(responses)}')

