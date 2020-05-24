from flask import render_template, flash, redirect, url_for, jsonify, json, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, CategoryForm, EditProfileForm
from app.models import User, Question
from sqlalchemy import func
from sqlalchemy.sql import exists  
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

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


@app.route('/admin')
@login_required
#NEED TO ADD PROTECTIONS TO THIS URL -> NOT ALLOW ACCESS UNLESS CREDENTIALED LOGIN W/ CORRECT PERMISSIONS
# Redirect to index if not correct user
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

@app.route('/category', methods = ['GET', 'POST'])
def category():
    cat = [('Sport','Sport'), ('General','General'), ('Food','Food')]
    form = CategoryForm()
    form.categories.choices = cat
    result = form.categories.data

    if form.is_submitted():
        if result != None:
            flash(result)
            user = User.query.filter_by(id=1)
            q = ['1','2']
            a = [('1','2','3','4'),('1','2','3','4')]
            ac = ['1','4']
            quest = {
                "username": str(user[0].username),
                "questions": q,
                "answers": a,
                "correct answers": ac
            }
            x = json.dumps(quest)
            session['request'] = x


             #q = Question.query.filter_by(category=result).order_by(func.random()).limit(10)
            z = Question.query.filter_by(category = result).order_by(func.random()).limit(5)
            q = []
            for i in range(0,4):
                q[i]
            return q
            x = session.query(QuestionAnswer.answer_id).filter_by(question_id = "x")
            x.filter_by(correct = True)


            #answers = QuestionAnswer.query.filter_by(questions.get_id() = answers.get_id()) 


            #quest = json.dumps({"username": str(user[0].username),"questions": q,"answers": a,})
            
            
            #for i in range(1,10):
                #quest = Question.query.filter_by(category=result).order_by(func.random()).limit(1)
                #q.append(str(quest.question))

            #quest = json.dumps({"username": str(user[0].username),"questions": q, }) # <--- not fully done yet.
            #answers = QuestionAnswer.query.filter_by(questions.get_id() = answers.get_id()) <--- Still needs to be done
            return(redirect(url_for('quiz')))
        else:
            flash(result)
            return(redirect(url_for('category')))


    return(render_template('category.html', form=form))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if db.session.query(exists().where(User.username == form.username.data)).scalar():
           flash("Username already taken!")
        else:
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Changed username to: ')
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    
    question_set = session.get('request')
    return question_set
    # Get the JSON from the server...
    # quizQuestions = request.json['questions']
    

   
    # THIS IS JUST USED TO LOAD A TEST JSON
    filename = os.path.join(app.static_folder, 'question.json')
    with open(filename) as jsonfile:
        rawdata = json.load(jsonfile)
        data = rawdata['questions']

    # REPLACE ABOVE WITH A DATABASE CALL

        questions = rawdata["questions"]
        answers = rawdata["answers"]
        corrAnswers = rawdata["correct answers"]


    return render_template("quiz.html", title="Quiz",   questions=questions,
                                                        answers=answers,
                                                        corrAnswers=corrAnswers)
                                                        