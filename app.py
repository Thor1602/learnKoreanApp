"""
Copyright prolog and class level copyright are included in this utility.
This file is intended for the development of comments.
The user can make changes to the text/prolog-text as appropriate.
This work is licensed under
a Creative Commons Attribution-ShareAlike 3.0 Unported License.
©Thorben, 2021
email: thorbendhaenenstd@gmail.com

"""
import re
from datetime import timedelta

from flask import Flask, render_template, session, redirect, url_for, flash, request, abort
from flask_ipban import IpBan
import Database
from os.path import exists

app = Flask(__name__)
app.static_folder = 'static'
main = Database.Main()
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
ip_ban = IpBan(ban_seconds=60, ban_count=5)
ip_ban.init_app(app)

if exists('secret_key.txt'):
    app.config['SECRET_KEY'] = open('secret_key.txt', 'r').read()
else:
    app.config['SECRET_KEY'] = main.get_secret_key()


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
        database_data = main.read_database()
        return render_template('admin_overview.html', database_data=database_data)


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
                elif key == "quizname564151154":
                    quiz = Database.Quiz(request.form['quizName'], request.form['quizType'])
                    quiz.register_quiz()
                elif key == 'question551531822':
                    question = Database.Question(request.form['quizNameChoice'], request.form['question'],
                                                 request.form['answerone'], request.form['answertwo'],
                                                 request.form['answerthree'], request.form['answerfour'],
                                                 request.form['correctanswer'])
                    question.register_question()
                elif key == 'translation465198155':
                    one_on_one_translation = Database.TranslationKorEng(request.form['quizNameChoiceTwo'],
                                                                        request.form['Korean'], request.form['English'])
                    one_on_one_translation.register_translation()
                elif key == "translation156151556":
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
        return render_template('quizmenu.html', quizzes=main.read_table('quiz'))


@app.route('/quiz<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if not session.get('logged_in'):
        flash('Login required')
        return redirect(url_for('login'))
    else:
        if main.get_quiz_type(quiz_id) == 'translate_to_Kor':
            quiz_data = main.get_quiz_to_Korean(quiz_id)
            quiz_questions = main.translation_quiz(quiz_data[0], quiz_data[1])
            number_of_questions = len(quiz_questions)
            if request.method == 'POST':
                question_with_answers = quiz_data[0]
                quiz_review = {}
                score = 0
                for question in request.form:
                    if question in question_with_answers:
                        if request.form[question] == question_with_answers[question]:
                            score += 1
                            quiz_review[question] = {'given answer: ': request.form[question],
                                                     'correct answer': question_with_answers[question], 'score': 1}
                        else:
                            quiz_review[question] = {'given answer: ': request.form[question],
                                                     'correct answer': question_with_answers[question], 'score': 0}
                user_id = main.get_user_id(session['current_user'])
                grades = Database.Grades(1, quiz_id, user_id, score, number_of_questions)
                grades.register_grades()
                session['grade_id'] = grades.get_id_currval()
                for question, results in quiz_review.items():
                    review = Database.Review(gradeID=session['grade_id'], userID=user_id, question=question,
                                             given_answer=results['given answer: '],
                                             correct_answer=results['correct answer'], score=results['score'])
                    review.register_review()
                return redirect(url_for('quizresult'))
            if len(quiz_questions) == 0:
                flash("There are no questions for this topic. ")
                return redirect(url_for('quizmenu'))
            else:
                return render_template('quiz_t.html', quiz_id=quiz_id, quiz_questions=quiz_questions)

        elif main.get_quiz_type(quiz_id) == 'translate_to_Eng':
            quiz_data = main.get_quiz_to_English(quiz_id)
            quiz_questions = main.translation_quiz(quiz_data[0], quiz_data[1])
            number_of_questions = len(quiz_questions)
            if request.method == 'POST':
                question_with_answers = quiz_data[0]
                quiz_review = {}
                score = 0
                for question in request.form:
                    if question in question_with_answers:
                        if request.form[question] == question_with_answers[question]:
                            score += 1
                            quiz_review[question] = {'given answer: ': request.form[question], 'correct answer': question_with_answers[question], 'score': 1}
                        else:
                            quiz_review[question] = {'given answer: ': request.form[question], 'correct answer': question_with_answers[question], 'score': 0}
                user_id = main.get_user_id(session['current_user'])
                grades = Database.Grades(1, quiz_id, user_id, score, number_of_questions)
                grades.register_grades()
                session['grade_id'] = grades.get_id_currval()
                for question, results in quiz_review.items():
                    review = Database.Review(gradeID=session['grade_id'], userID=user_id, question=question, given_answer=results['given answer: '], correct_answer= results['correct answer'], score=results['score'])
                    review.register_review()
                return redirect(url_for('quizresult'))
            if len(quiz_questions) == 0:
                flash("There are no questions for this topic. ")
                return redirect(url_for('quizmenu'))
            else:
                return render_template('quiz_t.html', quiz_id=quiz_id, quiz_questions=quiz_questions)

        elif main.get_quiz_type(quiz_id) == 'short_answers':
            quiz_data = main.get_short_quiz(quiz_id)
            number_of_questions = len(quiz_data)
            if request.method == 'POST':
                quiz_review = {}
                score = 0
                for question in request.form:
                    if question in quiz_data:
                        if request.form[question] == quiz_data[question]['correct_answer']:
                            score += 1
                            quiz_review[question] = {'given answer: ': request.form[question],
                                                     'correct answer': quiz_data[question]['correct_answer'], 'score': 1}
                        else:
                            quiz_review[question] = {'given answer: ': request.form[question],
                                                     'correct answer': quiz_data[question]['correct_answer'], 'score': 0}
                user_id = main.get_user_id(session['current_user'])
                grades = Database.Grades(1, quiz_id, user_id, score, number_of_questions)
                grades.register_grades()
                session['grade_id'] = grades.get_id_currval()
                for question, results in quiz_review.items():
                    review = Database.Review(gradeID=session['grade_id'], userID=user_id, question=question,
                                             given_answer=results['given answer: '],
                                             correct_answer=results['correct answer'], score=results['score'])
                    review.register_review()
                return redirect(url_for('quizresult'))
            if len(quiz_data) == 0:
                flash("There are no questions for this topic. ")
                return redirect(url_for('quizmenu'))
            else:
                return render_template('quiz_sa.html', quiz_id=quiz_id, quiz_questions=quiz_data)

        elif main.get_quiz_type(quiz_id) == 'long_answers':
            quiz_data = main.get_long_quiz(quiz_id)
            number_of_questions = len(quiz_data)
            if request.method == 'POST':
                quiz_review = {}
                score = 0
                for question in request.form:
                    if question in quiz_data:
                        if request.form[question] == quiz_data[question]['correct_answer']:
                            score += 1
                            quiz_review[question] = {'given answer: ': request.form[question],
                                                     'correct answer': quiz_data[question]['correct_answer'],
                                                     'score': 1}
                        else:
                            quiz_review[question] = {'given answer: ': request.form[question],
                                                     'correct answer': quiz_data[question]['correct_answer'],
                                                     'score': 0}
                user_id = main.get_user_id(session['current_user'])
                grades = Database.Grades(1, quiz_id, user_id, score, number_of_questions)
                grades.register_grades()
                session['grade_id'] = grades.get_id_currval()
                for question, results in quiz_review.items():
                    review = Database.Review(gradeID=session['grade_id'], userID=user_id, question=question,
                                             given_answer=results['given answer: '],
                                             correct_answer=results['correct answer'], score=results['score'])
                    review.register_review()
                return redirect(url_for('quizresult'))
            if len(quiz_data) == 0:
                flash("There are no questions for this topic. ")
                return redirect(url_for('quizmenu'))
            else:
                return render_template('quiz_la.html', quiz_id=quiz_id, quiz_questions=quiz_data)

        else:
            abort(400)


@app.route('/quizresult', methods=['GET', 'POST'])
def quizresult():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        user_id = main.get_user_id(session['current_user'])
        result = main.get_quiz_results(userid=user_id, gradeid=session['grade_id'])
        return render_template('quizresult.html', result=result)


@app.route('/discussion_overview', methods=['GET', 'POST'])
def discussion_overview():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        topics = main.read_table('discussion')
        return render_template('discussion_overview.html', topics=topics)

@app.route('/discussion_<discussion_id>', methods=['GET', 'POST'])
def discussion(discussion_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        all_discussion_queries = main.get_all_discussion_queries(discussion_id=discussion_id)
        return render_template('discussion.html', all_discussion_queries=all_discussion_queries)

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        name = main.get_user_name(session['current_user'])
        user_id = main.get_user_id(session['current_user'])
        grades_data = main.get_grades(user_id)
        return render_template('mypage.html', name=name, grades_data=grades_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')
    else:
        new_user = Database.User(request.form['nickname'], request.form['password'], 'Member',
                                 request.form['first_name'], request.form['last_name'], request.form['email'])
        if new_user.user_exists():
            flash("Email already exists.")
            return redirect(url_for('register'))
        if len(request.form['password']) < 8:
            flash("Password needs to be longer than 8 characters")
            return redirect(url_for('register'))
        if request.form['password'] != request.form['password_confirm']:
            flash("Passwords don't match")
            return redirect(url_for('register'))
        new_user.register_user()
        if main.verify_admin(request.form['email']):
            session['logged_in_admin'] = True
        session['logged_in'] = True
        session['current_user'] = request.form['email']
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session.clear()
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
            ip_ban.add()
            flash("incorrect credentials")
            return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


# @app.route('/admin_overview_js', methods=['GET', 'POST'])
# def admin_overview_js ():
#     if not session.get('logged_in_admin'):
#         flash('admin login credentials are required')
#         return redirect(url_for('login'))
#     else:
#         translation_data = main.read_table('translationkoreng')
#         discussion_data = main.read_table('discussion')
#         post_data = main.read_table('post')
#         reply_data = main.read_table('reply')
#         subreply_data = main.read_table('subreply')
#         question_data = main.read_table('question')
#         quiz_data = main.read_table('quiz')
#
#         return render_template('admin_overview.js', translation_data=translation_data,
#                                discussion_data=discussion_data, post_data=post_data, question_data=question_data,
#                                quiz_data=quiz_data, reply_data=reply_data, subreply_data=subreply_data)


@app.errorhandler(400)
def bad_request(e):
    e_friendly = "The server and client lost their manners"
    return render_template('error.html', e=e, e_friendly=e_friendly), 400


@app.errorhandler(403)
def forbidden(e):
    e_friendly = "A forbidden resource"
    return render_template('error.html', e=e, e_friendly=e_friendly), 403


@app.errorhandler(404)
def not_found(e):
    e_friendly = "Chap, you made a mistake typing that URL"
    return render_template('error.html', e=e, e_friendly=e_friendly), 404


@app.errorhandler(410)
def gone(e):
    e_friendly = "The page existed but is deleted and sent to Valhalla for all eternity."
    return render_template('error.html', e=e, e_friendly=e_friendly), 410


@app.errorhandler(500)
def internal_server_error(e):
    e_friendly = "'Server problems' To be overloaded or not to be overloaded. That's the question."
    return render_template('error.html', e=e, e_friendly=e_friendly), 500
