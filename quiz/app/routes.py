from flask import render_template, flash, redirect, url_for, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, CategoryForm, AddQuestionSetForm
from app.models import User, Question, Answer, QuestionAnswer
from sqlalchemy import func

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
    return(render_template("admin-addset.html", form=form))


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
