import numpy as np
import pandas as pd
from app import app,db
from app.models import User,Question,Answer,QuestionAnswer

dfuser = pd.read_csv('dbfill/user.csv', delimiter = ',',header=None,skipinitialspace = True)
print(dfuser)
dfquestion = pd.read_csv('dbfill/question.csv', delimiter = ',',header=None,skipinitialspace = True)
print(dfquestion)
dfanswer = pd.read_csv('dbfill/answer.csv',  delimiter = ',',header=None,skipinitialspace = True)
print(dfanswer)
dfmiddle = pd.read_csv('dbfill/questionanswer.csv',  delimiter = ',',header=None,skipinitialspace = True)
print(dfmiddle)

try:
    db.session.query(User).delete()
    db.session.query(Question).delete()
    db.session.query(Answer).delete()
    db.session.query(QuestionAnswer).delete()
except:
    print("no db to delete")

db.create_all()

for index, row in dfuser.iterrows():
    u = User(id = row[0], username = row[1], admin = row[3], email = row[4])
    u.set_password(row[2])
    db.session.add(u)
    db.session.commit()

for index, row in dfquestion.iterrows():
    u = Question(id = row[0], question = row[1], category = row[2], num_pres = row[3])
    #d = db.session.query(Question)
    #print(d.get(1))
    db.session.add(u)
    db.session.commit()
    
for index, row in dfanswer.iterrows():
    u = Answer(id = row[0], answer = row[1])
    db.session.add(u)
    db.session.commit()

for index, row in dfmiddle.iterrows():
    u = QuestionAnswer(id = row[0], question_id = row[1], answer_id = row[2], correct = row[3], num_picked = row[1])
    db.session.add(u)
    db.session.commit()
