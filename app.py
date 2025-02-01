from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'simulatore_dsga'

# Caricare la banca dati dei quiz
quiz_df = pd.read_excel("quiz_concorso_dsga_1000.xlsx")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    session['questions'] = quiz_df.sample(10).to_dict(orient='records')  # 10 domande casuali
    session['score'] = 0
    session['current_question'] = 0
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'questions' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('result'))

    question_data = session['questions'][session['current_question']]
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer == question_data['Risposta_Corretta']:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('question'))

    return render_template('question.html', question=question_data, q_number=session['current_question'] + 1)

@app.route('/result')
def result():
    score = session.get('score', 0)
    return render_template('result.html', score=score, total=len(session.get('questions', [])))

if __name__ == '__main__':
    app.run(debug=True)
