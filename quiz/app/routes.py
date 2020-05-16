from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
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

@app.route('/category', methods = ['GET', 'POST'])
def category()
    form=CategoryForm()
    if form.validate_on_submit():
        result = form.category.data
        if current_user.is_authenitcated():
            data = json.dumps({'username': current_user.get_id(), 'category': result})
            user = User.query.get(int(current_user.get_id()))
            questions = Question.query.filter_by(category=data.category).order_by(func.random()).limit(10)
            answers = QuestionAnswer.query.filter_by(questions.get(id) = answers.get(id))
            questionaire = json.dumps(questions.__dict__, answers.__dict__)
            return redirect(url_for('quiz'))
        else:
            flash("Username is not authenticated")
    return(render_template('category.html', form=form))
    
    

    

        
