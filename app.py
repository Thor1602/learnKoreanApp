"""
Copyright prolog and class level copyright are included in this utility.
This file is intended for the development of comments.
The user can make changes to the text/prolog-text as appropriate.
This work is licensed under
a Creative Commons Attribution-ShareAlike 3.0 Unported License.
©Thorben, 2021
email: thorbendhaenenstd@gmail.com

"""

from flask import Flask, render_template, session, redirect, url_for, flash, request
import Database

app = Flask(__name__)

app.secret_key = str(open("secret_key.txt", 'r').read())


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in_admin'):
        flash('admin login credentials are required')
        return redirect(url_for('login'))
    else:
        main = Database.Main()
        if request.method == "POST":
            for key in request.form:
                if key == 'discussion651554661':
                    discussion = Database.Discussion(request.form['discussionTopic'],
                                                     request.form['discussionQuestion'], main.get_user_id(session['current_user']))
                if key == "quizname564151154":
                    quiz = Database.Quiz(request.form['quizName'])
                    quiz.register_quiz()
                if key == 'question551531822':
                    question = Database.Question(request.form['quizNameChoice'], request.form['question'],
                                                 request.form['answerone'], request.form['answertwo'],
                                                 request.form['answerthree'], request.form['answerfour'],
                                                 request.form['correctanswer'])

                if key == 'translation465198155':
                    one_on_one_translation = Database.TranslationKorEng(request.form['quizNameChoiceTwo'], request.form['Korean'], request.form['English'])
                    one_on_one_translation.register_translation()
                if key == "translation156151556":
                    list_translation = request.form['translationlist']
                    list_translation = list_translation.split('\r\n')
                    for x in list_translation:
                        x = x.split(',')
                        translation = Database.TranslationKorEng(request.form['quizNameChoiceThree'], x[0], x[1])
                        translation.register_translation()

            return redirect(url_for('admin'))
        quiz_subjects = main.get_quiz_subjects()
        return render_template('admin.html', quiz_subjects=quiz_subjects)


@app.route('/quizmenu', methods=['GET', 'POST'])
def quizmenu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('quizmenu.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            print(request.form)
            return redirect(url_for('quizresult'))
        return render_template('quiz.html')


@app.route('/quizresult', methods=['GET', 'POST'])
def quizresult():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('quizresult.html')


@app.route('/discussion', methods=['GET', 'POST'])
def discussion():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('discussion.html')


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('mypage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session['logged_in'] = False
        session['logged_in_admin'] = False
        return render_template('login.html')
    elif request.method == 'POST':
        main = Database.Main()
        if main.verify_password(request.form['emaillogin'], request.form['passwordlogin']):
            session['logged_in'] = True
            if main.verify_admin(request.form['emaillogin']):
                session['logged_in_admin'] = True
            session['current_user'] = request.form['emaillogin']
            main.update_last_login(main.get_user_id(session['current_user']))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['logged_in_admin'] = False
    return redirect(url_for('login'))


@app.errorhandler(400)
def bad_request(e):
    e_friendly = "The server and client don't seem to have any manners"
    return render_template('error.html', e=e, e_friendly=e_friendly), 400


@app.errorhandler(403)
def forbidden(e):
    e_friendly = "a forbidden resource"
    return render_template('error.html', e=e, e_friendly=e_friendly), 403


@app.errorhandler(404)
def not_found(e):
    e_friendly = "chap, you made a mistake typing that URL"
    return render_template('error.html', e=e, e_friendly=e_friendly), 404


@app.errorhandler(410)
def gone(e):
    e_friendly = "The page existed but is deleted and sent to Valhalla for all eternity."
    return render_template('error.html', e=e, e_friendly=e_friendly), 410


@app.errorhandler(500)
def internal_server_error(e):
    e_friendly = "'server problems' To be overloaded or not to be overloaded. That's the question."
    return render_template('error.html', e=e, e_friendly=e_friendly), 500
