from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
<<<<<<< HEAD
    return "Hello World"

#test
=======
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/admin')
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
>>>>>>> 62e37b597fcca98deba971da8f83c86392aefb0f
