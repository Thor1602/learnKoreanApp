import os
import random

from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import Error
import psycopg2


class Main:
    """
        This main class of the database helper is:
            - to execute all types of queries
            - read a table in the database
            - delete an entry in a table in the database
    """

    def execute_query(self, query_list, commit=False, fetchAll=False, fetchOne=False):
        try:
            # credentials = str(open("database_credentials.txt", 'r').read())
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            c = conn.cursor()
            result = None
            if type(query_list) == str:
                c.execute(query_list)
            elif isinstance(query_list, tuple):
                c.execute(query_list[0], query_list[1])
            else:
                for query in query_list:
                    if isinstance(query, tuple):
                        c.execute(query[0], query[1])
                    else:
                        c.execute(query)
            if commit:
                conn.commit()
            if fetchAll:
                result = [row for row in c.fetchall()]
            if fetchOne:
                result = c.fetchone()
            c.close()
            conn.close()
            return result

        except Error as e:
            print(e)

    def read_table(self, table_name):
        return self.execute_query(query_list=f"SELECT * FROM {table_name}", fetchAll=True)

    def read_database(self):
        database = {}
        database['translation_data'] = self.read_table('translationkoreng')
        database['discussion_data'] = self.read_table('discussion')
        database['post_data'] = self.read_table('post')
        database['reply_data'] = self.read_table('reply')
        database['subreply_data'] = self.read_table('subreply')
        database['question_data'] = self.read_table('question')
        database['quiz_data'] = self.read_table('quiz')

        database['translation_columns'] = self.read_columns('translationkoreng')
        database['discussion_columns'] = self.read_columns('discussion')
        database['post_columns'] = self.read_columns('post')
        database['reply_columns'] = self.read_columns('reply')
        database['subreply_columns'] = self.read_columns('subreply')
        database['question_columns'] = self.read_columns('question')
        database['quiz_columns'] = self.read_columns('quiz')
        return database

    def read_columns(self, db_name):
        return self.execute_query(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + db_name + "';", fetchAll=True)

    def del_comment(self, id, db_name):
        self.execute_query(query_list=f'DELETE FROM {db_name} WHERE id = {id}', commit=True)

    def add_column(self, table_name, new_column_name, column_definition):
        self.execute_query(f"ALTER TABLE {table_name} ADD {new_column_name} {column_definition};", commit=True)

    def verify_password(self, email, pwd):
        retrieved_password = \
            self.execute_query(query_list=f"SELECT password FROM users where email = '{email}'", fetchAll=True)[0][0]
        return check_password_hash(retrieved_password, pwd)

    def verify_admin(self, email):
        role = self.execute_query(query_list=f"SELECT role_name FROM users where email = '{email}'", fetchAll=True)[0][
            0]
        if role == "Administrator":
            return True
        else:
            return False

    def generate_hash(self, pwd):
        return generate_password_hash(pwd)

    def get_user_id(self, email):
        return self.execute_query(query_list=f"SELECT ID from users where email = '{email}'", fetchOne=True)[0]

    def get_user_name(self, email):
        return self.execute_query(
            query_list=f"SELECT first_name, last_name, nickname from users where email = '{email}'", fetchAll=True)

    def get_user_email(self, id):
        global email
        try:
            email = self.execute_query(query_list=f"SELECT email from users where id = '{id}'", fetchOne=True)[0]
        except TypeError as e:
            email = None
        finally:
            return email

    def get_user_data(self, id):
        return self.execute_query(query_list=f"SELECT * from users where id = '{id}'", fetchAll=True)[0]

    def update_last_login(self, id):
        self.execute_query(query_list=F"UPDATE users SET last_login = NOW() where id = {id}", commit=True)

    def get_secret_key(self):
        return self.execute_query(query_list="SELECT value from settings where key = 'secret_key'", fetchOne=True)[0]

    def get_quiz_subjects(self):
        return [(x[0], x[1]) for x in self.read_table('quiz')]

    def get_quiz_type(self, id):
        return self.execute_query(query_list=f"SELECT type from quiz where id = '{id}'", fetchAll=True)[0][0]

    def alter_password(self, email, old_pwd, new_pwd):
        # "23FvMIs*5cx8fHRv"
        new_pwd = generate_password_hash(new_pwd)
        if self.verify_password(email, old_pwd):
            self.execute_query(query_list=f"UPDATE users SET password = '{new_pwd}' where email = '{email}'",
                               commit=True)
            return True
        else:
            return False

    def get_quiz_to_English(self, quizid):
        questions_with_answer, all_answers = {}, []
        for x in self.execute_query(query_list=f"SELECT * from translationkoreng where quizid = {quizid}",
                                    fetchAll=True):
            questions_with_answer[x[1]] = x[2]
            all_answers.append(x[2])
        random.shuffle(all_answers)
        return (questions_with_answer, all_answers)

    def get_quiz_to_Korean(self, quizid):
        questions_with_answer, all_answers = {}, []
        for x in self.execute_query(query_list=f"SELECT * from translationkoreng where quizid = {quizid}",
                                    fetchAll=True):
            questions_with_answer[x[2]] = x[1]
            all_answers.append(x[1])
        random.shuffle(all_answers)
        return (questions_with_answer, all_answers)

    def translation_quiz(self, questions_with_answer, all_answers):
        questions = {}
        for x in questions_with_answer:
            answers, count, index = [], 0, 0
            answers.append(questions_with_answer[x])
            answers = answers + random.sample(all_answers, 3)
            random.shuffle(answers)
            questions[x] = answers
            random.shuffle(all_answers)
        return questions

    def get_quiz_name(self, id):
        return self.execute_query(query_list=f"SELECT name from quiz where id = '{id}'", fetchOne=True)[0]

    def get_grades(self, userID):
        query = self.execute_query(
            query_list=f"SELECT id, courseid, quizid, score, total_score, date_trunc('minute', date) from grades where userid = {userID} ORDER BY date DESC;",
            fetchAll=True)
        modified_query = []
        for row in query:
            row = [x for x in row]
            modified_query.append(row)
        for row in modified_query:
            row[2] = self.get_quiz_name(row[2])
        return modified_query

    def get_quiz_results(self, userid, gradeid):
        grade = \
        self.execute_query(query_list=f"SELECT * FROM grades WHERE userid = {userid} ORDER BY date DESC LIMIT 1;",
                           fetchAll=True)[0]
        review = self.execute_query(query_list=f"SELECT * FROM reviews WHERE gradeid = {gradeid}", fetchAll=True)
        return grade, review


class User(Main):
    def __init__(self, nickname, password, role, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.password = generate_password_hash(password)
        self.role_name = role
        self.email = email

    def register_user(self):
        self.execute_query(
            query_list=f"INSERT INTO users (first_name, last_name, nickname, password, role_name, email, last_login, created_on) VALUES ('{self.first_name}', '{self.last_name}', '{self.nickname}', '{self.password}', '{self.role_name}', '{self.email}', NOW(), NOW());",
            commit=True)

    def user_exists(self):
        return self.execute_query(query_list=f"SELECT exists(select 1 from users where email = '{self.email}')",
                                  fetchOne=True)[0]


class UserCourse(Main):
    def __init__(self, userID, CourseID):
        self.userID = userID
        self.CourseID = CourseID


class Course(Main):
    def __init__(self, name):
        self.name = name

    def register_course(self):
        self.execute_query(
            query_list=f"INSERT INTO course (name) VALUES ('{self.name}')", commit=True)


class Quiz(Main):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def register_quiz(self):
        self.execute_query(
            query_list=f"INSERT INTO quiz (name) VALUES ('{self.name}')", commit=True)

    def update_quiz_type(self, name):
        self.execute_query(
            query_list=f"UPDATE quiz SET type = '{self.type}' WHERE name = '{name}'", commit=True)

    def update_quiz(self, id):
        self.execute_query(
            query_list=f"UPDATE quiz SET name = '{self.name}', type = '{self.type}' WHERE ID = {id}", commit=True)


class Question(Main):
    def __init__(self, quizID, question, answer_one, answer_two, answer_three, answer_four, correct_answer, image_id=0):
        self.quizID = quizID
        self.question = question
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.answer_three = answer_three
        self.answer_four = answer_four
        self.correct_answer = correct_answer
        self.image_id = image_id

    def register_question(self):
        self.execute_query(
            query_list=f"INSERT INTO question (quizID, question, answer_one, answer_two, answer_three, answer_four, correct_answer, image_id) VALUES ({self.quizID}, '{self.question}', '{self.answer_one}', '{self.answer_two}', '{self.answer_three}', '{self.answer_four}', '{self.correct_answer}', {self.image_id});",
            commit=True)


class TranslationKorEng(Main):
    def __init__(self, quizID, Korean, English, image_id=0):
        self.Korean = Korean
        self.English = English
        self.quizID = quizID
        self.image_id = image_id

    def register_translation(self):
        self.execute_query(
            query_list=f"INSERT INTO translationkoreng (korean, english, quizid, image_id) VALUES ('{self.Korean}', '{self.English}', '{self.quizID}', {self.image_id})",
            commit=True)


class Grades(Main):
    def __init__(self, courseID, QuizID, userID, score, total_score):
        self.courseID = courseID
        self.QuizID = QuizID
        self.userID = userID
        self.score = score
        self.total_score = total_score

    def register_grades(self):
        self.execute_query(
            query_list=f"INSERT INTO grades (courseID, quizID, userID, score, total_score, date) VALUES ({self.courseID}, {self.QuizID}, {self.userID}, {self.score}, {self.total_score}, NOW())",
            commit=True)

    def get_id_currval(self):
        return self.execute_query(query_list=f"SELECT id FROM grades ORDER BY date DESC LIMIT 1;", fetchOne=True)[0]


class Review(Main):
    def __init__(self, gradeID, userID, question, given_answer, correct_answer, score):
        self.gradeID = gradeID
        self.userID = userID
        self.question = question
        self.given_answer = given_answer
        self.correct_answer = correct_answer
        self.score = score

    def register_review(self):
        self.execute_query(
            query_list=f"INSERT INTO reviews (gradeID, userID, question, given_answer, correct_answer, score) VALUES ({self.gradeID}, {self.userID}, '{self.question}', '{self.given_answer}', '{self.correct_answer}', '{self.score}')",
            commit=True)


class Discussion(Main):
    def __init__(self, topic, question, userID, image_id=0):
        self.topic = topic
        self.question = question
        self.userID = userID
        self.image_id = image_id

    def register_discussion(self):
        self.execute_query(
            query_list=f"INSERT INTO discussion (topic, date, userid, image_id, question) VALUES ('{self.topic}', NOW(), {self.userID}, {self.image_id}, '{self.question}')",
            commit=True)


class Post(Main):
    def __init__(self, post, discussionID, userID):
        self.post = post
        self.discussionID = discussionID
        self.userID = userID

    def register_post(self):
        self.execute_query(
            query_list=f"INSERT INTO post (post, date, discussionid, userid) VALUES ('{self.post}', NOW(), {self.discussionID}, {self.userID})",
            commit=True)


class Reply(Main):
    def __init__(self, reply, postID, userID):
        self.reply = reply
        self.postID = postID
        self.userID = userID

    def register_reply(self):
        self.execute_query(
            query_list=f"INSERT INTO reply (reply, date, postid, userid) VALUES ('{self.reply}', NOW(), {self.postID}, {self.userID})",
            commit=True)


class SubReply(Main):
    def __init__(self, subreply, replyID, userID):
        self.subreply = subreply
        self.replyID = replyID
        self.userID = userID

    def register_subreply(self):
        self.execute_query(
            query_list=f"INSERT INTO subreply (subreply, date, replyid, userid) VALUES ('{self.subreply}', NOW(), {self.replyID}, {self.userID})",
            commit=True)
