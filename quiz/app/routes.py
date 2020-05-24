from flask import render_template, flash, redirect, url_for, jsonify, json, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, CategoryForm, AddQuestionSetForm
from app.models import User, Question, Answer, QuestionAnswer
from sqlalchemy import func
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

 # user login/registration content 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #User already signed in -> shouldn't be able to login again       
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        form.validate()
        user =User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Error: Invalid credentials") 
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #User already signed in -> shouldn't be able to register an account.
        return redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        #check if user already exists in database
        form.validate()
        present = User.query.filter_by(username=form.username.data).first()
        if present is not None:
            flash("Error: This username is taken")
            return render_template("register.html", form=form)
        user = User (username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration Completed!") #FLASH NOT WORKING?!?!?!?!?!
        return redirect(url_for('login'))
    return(render_template('register.html', form=form))

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))
# end user login/register content
# Admin content

@app.route('/admin')
@login_required
def admin():
    if (current_user.is_admin() == False):
        return "Access Denied"
    return render_template("admin-splash.html")

@app.route('/admin/adduser', methods=['GET', 'POST'])
@login_required
def admin_adduser():
    if (current_user.is_admin() == False):
        return "Access Denied"      
    form = AddUserForm()
    
    if form.validate_on_submit():
        form.validate()
        #check if user already exists in database
        present = User.query.filter_by(username=form.username.data).first()
        if present is not None:
            flash("Error: This user already exists")
            return render_template("admin-adduser.html", form=form)
        user = User(username=form.username.data, admin=form.admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User Succesfully Created!") 
        return redirect(url_for('admin'))
    return(render_template('admin-adduser.html', form=form))

@app.route('/admin/viewuser')
@login_required
def admin_viewusers():
    if (current_user.is_admin() == False):
        return "Access Denied"
    Users= User.query.all()
    return render_template("admin-viewuser.html", Users=Users)

@app.route('/admin/edituser', methods=["GET", "POST"])
@login_required
def admin_edituser():
    if(current_user.is_admin() == False):
        return "Access Denied"
    form=EditUserForm()
    if form.validate_on_submit():
        form.validate()
        #Check if user exists in database and can be modified
        present = User.query.filter_by(username=form.old_username.data).first()
        if present is None:
            flash("Error: This user does not exist in the database")
            return render_template("admin-edit.html", form=form)
        old_user = form.old_username.data
        #delete record from database unless it is the admin account or the current user
        if (form.delete.data) == True:
            if form.old_username.data == "admin":
                flash("Error: This user cannot be removed from the database")
                return render_template("admin-edit.html", form=form)
            elif current_user.username == old_user:
                flash("Error: Cannot delete the user currently signed in.")
                return render_template("admin-edit.html", form=form)
            else:
         
                User.query.filter_by(username=form.old_username.data).delete()
        #begin editing record
        if old_user:
            user=User.query.filter_by(username=form.old_username.data).first()
        else:
            flash("Error: No user selected for editing")
            return render_template("admin-edit.html", form=form)
        if old_user == "admin":
            flash("Error: Cannot modify admin!")
            return render_template("admin-edit.html", form=form)
        new_user = form.new_username.data
        if new_user:
            user.username = form.new_username.data
        new_password = form.password_confirm.data
        if new_password:
            user.set_password(form.password.data)
        email =  form.email.data
        if email:
            user.email=form.email.data
        admin=form.admin.data
        if admin:
            user.admin=form.admin.data  
        db.session.commit()
        flash("User succesfully modified")
        return redirect(url_for('admin'))
    return(render_template('admin-edit.html', form=form))

@app.route('/admin/addquestionset', methods=["GET", "POST"])
@login_required
def admin_addset():
    if(current_user.is_admin() == False):
        return "Access Denied"

    form=AddQuestionSetForm()
    if form.validate_on_submit():
        form.validate()
        #check to see if a category has been entered
        existing_category = form.existing_category.data
        new_category = form.new_category.data
        if not (existing_category or new_category):
            flash("Error: No category entered")
            return render_template('admin-addset.html', form=form)
        #Check if existing category data actually is present in database
        if existing_category and not new_category:
            present = Question.query.filter_by(category=form.existing_category.data).first()
            if present is None:
                flash("Error: Could not find existing category. Please try again.")
                return render_template("admin-addset.html", form=form)
        #check if question already exists in the database (questions should be unique)
        present = db.session.query(Question.id).filter_by(question=form.question.data).scalar() is not None
        if present:
            flash("Error: This question already exists. Delete the question if you are wishing to replace it.")
            return render_template("admin-addset.html", form=form)

        #Check if all answers are unique: Can cause issues if not
        answers =[]
        answers.append(form.answer.data)
        if form.fake_ans1.data in answers:
            flash("Error: Answer and fake answers must be unique.")
            return render_template("admin-addset.html", form=form)
        else:
            answers.append(form.fake_ans1.data)
            if form.fake_ans2.data in answers:
                flash("Error: Answer and fake answers must be unique.")
                return render_template("admin-addset.html", form=form)
            else:
                answers.append(form.fake_ans2.data)
                if form.fake_ans3.data in answers:
                    flash("Error: Answer and fake answers must be unique.")
                return render_template("admin-addset.html", form=form)

        #load in form data and prepare to submit to database       
        question = Question(question=form.question.data)
        if existing_category:
            question.category = form.existing_category.data
        else:
            question.category = form.new_category.data
        answer = Answer(answer=form.answer.data)
        #commit to db to allow for QuestionAnswer relationtable to be updated.
        db.session.add(question)
        db.session.add(answer)
        db.session.commit()
        #update Question/Answer with correct ans:
        questionanswer = QuestionAnswer(question_id=question.id, answer_id =answer.id, correct=True, num_picked=0)
        db.session.add(questionanswer)
        db.session.commit()
        #add in incorrect answers to answer table
        incorrect1 = Answer(answer=form.fake_ans1.data)
        incorrect2 = Answer(answer=form.fake_ans2.data)
        incorrect3 = Answer(answer=form.fake_ans2.data)
        db.session.add(incorrect1)
        db.session.add(incorrect2)
        db.session.add(incorrect3)
        db.session.commit()
        #updating question/answer with incorrect questions
        incorrectquestionanswer1 = QuestionAnswer(question_id=question.id, answer_id=incorrect1.id, correct = False, num_picked=0)
        incorrectquestionanswer2 = QuestionAnswer(question_id=question.id, answer_id=incorrect2.id, correct=False, num_picked=0)
        incorrectquestionanswer3 = QuestionAnswer(question_id=question.id, answer_id=incorrect3.id, correct=False, num_picked=0)
        db.session.add(incorrectquestionanswer1)
        db.session.add(incorrectquestionanswer2)
        db.session.add(incorrectquestionanswer3)
        db.session.commit()
        #Question set now added to db.
        flash("Question set added!")
        return(redirect(url_for('index')))
    return(render_template('admin-addset.html', form=form))


#quiz content
@app.route('/category', methods = ['GET', 'POST'])
def category():
    form = CategoryForm()
    if form.is_submitted():
        cat_choices = ['Sport','Food','Music']
        result = form.categories.data
        for key in cat_choices:
            if(result in key):
                flash(result)

        return(redirect(url_for('index')))
        if current_user.is_authenticated:
            user = User.query.filter_by(id=1)
            q = []
            for i in range(1,10):
                quest = Question.query.filter_by(category=result).order_by(func.random()).limit(1)
                q.append(str(quest.question))

            quest = json.dumps({"username": str(user[0].username),"questions": q}) # <--- not fully done yet.
            #answers = QuestionAnswer.query.filter_by(questions.get_id() = answers.get_id()) <--- Still needs to be done
            return(redirect(url_for('index')))

    return(render_template('category.html', form=form))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    
    # Get the JSON from the server...
    # quizQuestions = request.json['questions']
    
    # THIS IS JUST USED TO LOAD A TEST JSON
    filename = os.path.join(app.static_folder, 'question.json')
    with open(filename) as jsonfile:
        rawdata = json.load(jsonfile)
        data = rawdata['questions']

    # REPLACE ABOVE WITH A DATABASE CALL

        q1 = data[0]
        q2 = data[1]
        q3 = data[2]
        q4 = data[3]
        q5 = data[4]
        q6 = data[5]
        q7 = data[6]
        q8 = data[7]
        q9 = data[8]
        q10 = data[9]

    return render_template("quiz.html", title="Quiz",   questions=data,
                                                        q1=q1,
                                                        q2=q2,
                                                        q3=q3,
                                                        q4=q4,
                                                        q5=q5,
                                                        q6=q6,
                                                        q7=q7,
                                                        q8=q8,
                                                        q9=q9,
                                                        q10=q10)
    

                            
