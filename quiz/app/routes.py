from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        flash("Account created for user {}, email= {}".format(form.username.data, form.email.data))
        return redirect(url_for('index'))
    return(render_template('register.html', form=form))