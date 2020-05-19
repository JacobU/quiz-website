from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegisterForm, AddUserForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

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
@login_required #add protections so only admin can access
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
        flash("User Created") #flash not working
        return redirect(url_for('admin'))
    return(render_template('admin-adduser.html', form=form))

@app.route('/admin/viewuser')
@login_required
def admin_viewusers():
    if (current_user.is_admin() == False):
        return "Access Denied"
    Users= User.query.all()
    return render_template("admin-viewuser.html", Users=Users)

