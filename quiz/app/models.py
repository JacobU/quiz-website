from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#initial version of database will store passwords. Store hashes later?
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    pword_h = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default = False)
    email = db.Column(db.String(128), index = True)
    userbio = db.Column(db.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    #Taken from flask mega tutorial
    def set_password(self, password):
        self.pword_h = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.pword_h, password)
    #check if a user has administrator priv
    def is_admin(self):
        return (self.admin == True)

#taken from flask mega tutorial
#finds user record in User table
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(128), unique = True)
    category = db.Column(db.String(32))
    num_pres = db.Column(db.Integer)

    def __repr__(self):
        return '<Question {}>'.format(self.question)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.String(32), unique = True)

    def __repr__(self):
        return '<Answer {}>'.format(self.answer)


#when assigning answers to questions make sure correct answers are specified
    #potential to cause error of no correct answers
class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    correct = db.Column(db.Boolean, default = False)
    num_picked = db.Column(db.Integer)
    
    #unsure if this will work with id
    def __repr__(self):
        return '<QuestionAnswer {}>'.format(self.id)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))

    #unsure if this will work with id
    def __repr__(self):
        return '<Quiz {}>'.format(self.id)

    



       