from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secretsecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    survey_keys = surveys.surveys.keys()
    return render_template('home.html', survey_keys=survey_keys) 

@app.route('/pick-survey', methods=['POST'])
def pick_survey():
    survey = request.form['survey-choice']
    session['survey'] = survey
    return redirect('/survey-page')

@app.route('/survey-page')
def show_survey_page():
    code = session['survey']
    survey = surveys.surveys[code]
    title = survey.title
    instructions = survey.instructions
    return render_template('survey-page.html', title=title, instructions=instructions)

@app.route('/set-session', methods=['POST'])
def set_session():
    session['responses'] = []
    session['counter'] = 0
    return redirect('/questions/0')

@app.route('/thanks')
def thanks_page():
    code = session['survey']
    survey = surveys.surveys[code]
    questions =  []
    for n in range(len(survey.questions)): 
        questions.append(survey.questions[n].question)
    responses = session['responses']
    q_and_a = zip(questions, responses)
    
    return render_template('thanks-page.html', q_and_a=q_and_a)

@app.route('/questions/<int:num>')
def show_questions(num):
    code = session['survey']
    survey = surveys.surveys[code]
    counter = session['counter']
    if num != counter:
        flash('Invalid Request', 'error')
        return redirect(f'/questions/{counter}')
    elif counter == len(survey.questions):
        return redirect('/thanks')
    else:
        question = survey.questions[num].question
        choices = survey.questions[num].choices
        allow_text = survey.questions[num].allow_text
        return render_template('question-page.html', question=question, choices=choices, num=num, allow_text=allow_text)

@app.route('/answer', methods=['POST'])
def handle_answer():
    code = session['survey']
    survey = surveys.surveys[code]
    comment = request.form.get('comment')
    if comment:
        answer = [request.form['choice'], comment]
    else: 
        answer = request.form['choice']
     
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    counter = session['counter']
    counter += 1
    session['counter'] = counter

    if len(survey.questions) == len(responses):
        return redirect('/thanks')
    else:
        return redirect(f'/questions/{counter}')

