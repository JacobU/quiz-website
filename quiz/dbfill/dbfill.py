import numpy as np
import pandas as pd
from app import app,db
from app.models import User,Question,Answer,QuestionAnswer

dfuser = pd.read_csv('user.csv')
dfquestion = pd.read_csv('question.csv')
dfanswer = pd.read_csv('answer.csv')
dfmiddle = pd.read_csv('questionanswer.csv')

for index, row in dfuser.iterrows():
    u = User(id = c1, username = c2, admin = c4, email = c5)
    u.set_password(c3)
    db.session.add(u)
    db.session.commit()

for index, row in dfuser.iterrows():
    u = Question(id = c1, question = c2, category = c3, numpres = c4)
    db.session.add(u)
    db.session.commit()
    
for index, row in dfuser.iterrows():
    u = Question(id = c1, answer = c2)
    db.session.add(u)
    db.session.commit()

for index, row in dfuser.iterrows():
    u = Question(id = c1, question_id = c2, answer_id = c3, correct = c4, numpicked = c5)
    db.session.add(u)
    db.session.commit()
