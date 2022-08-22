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
main = Database.Main()
app.secret_key = main.execute_query(query_list="SELECT value from settings where key = 'secret_key'", fetchOne=True)[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/admin_overview', methods=['GET', 'POST'])
def admin_overview():
    if not session.get('logged_in_admin'):
        flash('admin login credentials are required')
        return redirect(url_for('login'))
    else:
        translation_data = main.read_table('translationkoreng')
        discussion_data = main.read_table('discussion')
        post_data = main.read_table('post')
        reply_data = main.read_table('reply')
        subreply_data = main.read_table('subreply')
        question_data = main.read_table('question')
        quiz_data = main.read_table('quiz')
        translation_columns = main.read_columns('translationkoreng')
        discussion_columns = main.read_columns('discussion')
        post_columns = main.read_columns('post')
        reply_columns = main.read_columns('reply')
        subreply_columns = main.read_columns('subreply')
        question_columns = main.read_columns('question')
        quiz_columns = main.read_columns('quiz')

        return render_template('admin_overview.html', translation_data=translation_data,
                               discussion_data=discussion_data, post_data=post_data, question_data=question_data,
                               quiz_data=quiz_data, reply_data=reply_data, subreply_data=subreply_data, translation_columns=translation_columns,
                               discussion_columns=discussion_columns, post_columns=post_columns, question_columns=question_columns,
                               quiz_columns=quiz_columns, reply_columns=reply_columns, subreply_columns=subreply_columns)


@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if not session.get('logged_in_admin'):
        flash('admin login credentials are required')
        return redirect(url_for('login'))
    else:
        if request.method == "POST":
            for key in request.form:
                if key == 'discussion651554661':
                    discussion = Database.Discussion(topic=request.form['discussionTopic'],
                                                     question=request.form['discussionQuestion'],
                                                     userID=main.get_user_id(session['current_user']))
                    discussion.register_discussion()
                if key == "quizname564151154":
                    quiz = Database.Quiz(request.form['quizName'])
                    quiz.register_quiz()
                if key == 'question551531822':
                    question = Database.Question(request.form['quizNameChoice'], request.form['question'],
                                                 request.form['answerone'], request.form['answertwo'],
                                                 request.form['answerthree'], request.form['answerfour'],
                                                 request.form['correctanswer'])
                    question.register_question()
                if key == 'translation465198155':
                    one_on_one_translation = Database.TranslationKorEng(request.form['quizNameChoiceTwo'],
                                                                        request.form['Korean'], request.form['English'])
                    one_on_one_translation.register_translation()
                if key == "translation156151556":
                    list_translation = request.form['translationlist']
                    list_translation = list_translation.split('\r\n')
                    for x in list_translation:
                        x = x.split(',')
                        translation = Database.TranslationKorEng(request.form['quizNameChoiceThree'], x[0], x[1])
                        translation.register_translation()

            return redirect(url_for('admin_register'))
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

@app.route('/admin_overview_js', methods=['GET', 'POST'])
def admin_overview_js ():
    if not session.get('logged_in_admin'):
        flash('admin login credentials are required')
        return redirect(url_for('login'))
    else:
        translation_data = main.read_table('translationkoreng')
        discussion_data = main.read_table('discussion')
        post_data = main.read_table('post')
        reply_data = main.read_table('reply')
        subreply_data = main.read_table('subreply')
        question_data = main.read_table('question')
        quiz_data = main.read_table('quiz')

        return render_template('admin_overview.js', translation_data=translation_data,
                               discussion_data=discussion_data, post_data=post_data, question_data=question_data,
                               quiz_data=quiz_data, reply_data=reply_data, subreply_data=subreply_data)



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
