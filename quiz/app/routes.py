from flask import render_template, flash, redirect, url_for, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm, AddUserForm, CategoryForm
from app.models import User, Question
from sqlalchemy import func

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid credentials") #Flash not working????******
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
#NEED TO ADD PROTECTIONS TO THIS URL -> NOT ALLOW ACCESS UNLESS CREDENTIALED LOGIN W/ CORRECT PERMISSIONS
# Redirect to index if not correct user
def admin():
    return render_template("admin-splash.html")

@app.route('/admin/adduser', methods=['GET', 'POST'])
@login_required
def admin_adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, admin=form.admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User Created") #flash not working
        return redirect(url_for('admin'))
    return(render_template('admin-adduser.html', form=form))

@app.route('/admin/viewuser')
@login_required
def admin_viewusers():
    Users= User.query.all()
    return render_template("admin-viewuser.html", Users=Users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #User already signed in -> shouldn't be able to register an account.
        return redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        user = User (username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration Completed!") #FLASH NOT WORKING?!?!?!?!?!
        return redirect(url_for('login'))
    return(render_template('register.html', form=form))

@app.route('/category', methods = ['GET', 'POST'])
def category():
    form = CategoryForm()
    if form.is_submitted():
        flash("success!")
        result = form.categories.data
        return result
        if current_user.is_authenticated:
            user = User.query.filter_by(id=1)
            q = []
            for i in range(1,10):
                quest = Question.query.filter_by(category=result).order_by(func.random()).limit(1)
                q.append(str(quest.question))

            quest = json.dumps({"username": str(user[0].username),"questions": q})
            return quest
            #answers = QuestionAnswer.query.filter_by(questions.get_id() = answers.get_id())
            #return(redirect(url('index')))

    return(render_template('category.html', form=form))
    
    

    

        
