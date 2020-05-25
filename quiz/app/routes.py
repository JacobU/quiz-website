from flask import render_template, flash, redirect, url_for, jsonify, json, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, CategoryForm, AddQuestionSetForm, DeleteQuestionSetForm, EditProfileForm, SearchUserForm
from app.models import User, Question, Answer, QuestionAnswer, Quiz
from sqlalchemy import func
from sqlalchemy.sql import exists  
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
        flash("Login successful!")
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
        flash("Registration Completed!") 
        return redirect(url_for('index'))
    return(render_template('register.html', form=form))

@app.route('/signout')
def signout():
    logout_user()
    flash("Logout successful!")
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
        db.session.add(question)

        
        #check if answer is already in the answers table. If it isnt add to table. If present retrieve its ID and serve to question answer table
        present = db.session.query(Answer.id).filter_by(answer=form.answer.data).scalar() is not None
        if not present:
            #answer not present -> add to ans table and add relation
            answer = Answer(answer=form.answer.data)
            db.session.add(answer)
            db.session.commit()
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =answer.id, correct=True, num_picked=0)
        else:
            #answer present -> get ID and add relation
            answer =Answer.query.filter_by(answer=form.answer.data).first()
            answer_id =answer.id
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =answer_id, correct=True, num_picked=0)
        db.session.add(questionanswer)
        db.session.commit()
        
        
        #add in incorrect answers to answer table. Need to check an answer isnt already in the table due to table relations.
        #if incorrect ans is already in the database we need to grab its ID and store it.

        #process incorrect ans 1 using above logic.
        present = db.session.query(Answer.id).filter_by(answer=form.fake_ans1.data).scalar() is not None
        if not present:
            incorrect1 = Answer(answer=form.fake_ans1.data)
            db.session.add(incorrect1)
            db.session.commit()
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =incorrect1.id, correct=False, num_picked=0)
            db.session.add(questionanswer)
            db.session.commit()
        else:
            incorrect1 = Answer.query.filter_by(answer=form.fake_ans1.data).first()
            incorrect1_id = incorrect1.id
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =incorrect1_id, correct=False, num_picked=0)
        db.session.add(questionanswer)
        db.session.commit()

        #process incorrect ans 2 using above logic
        present = db.session.query(Answer.id).filter_by(answer=form.fake_ans2.data).scalar() is not None
        if not present:
            incorrect2 = Answer(answer=form.fake_ans2.data)
            db.session.add(incorrect2)
            db.session.commit()
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =incorrect2.id, correct=False, num_picked=0)
            db.session.add(questionanswer)
            db.session.commit()
        else:
            incorrect2 = Answer.query.filter_by(answer=form.fake_ans2.data).first()
            incorrect2_id = incorrect2.id
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =incorrect2_id, correct=False, num_picked=0)
        db.session.add(questionanswer)
        db.session.commit()

        #process incorrect ans 3 using above logic
        present = db.session.query(Answer.id).filter_by(answer=form.fake_ans3.data).scalar() is not None
        if not present:
            incorrect3 = Answer(answer=form.fake_ans3.data)
            db.session.add(incorrect3)
            db.session.commit()
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =incorrect3.id, correct=False, num_picked=0)
            db.session.add(questionanswer)
            db.session.commit()
        else:
            incorrect3 = Answer.query.filter_by(answer=form.fake_ans3.data).first()
            incorrect3_id = incorrect3.id
            questionanswer = QuestionAnswer(question_id=question.id, answer_id =incorrect3_id, correct=False, num_picked=0)
        db.session.add(questionanswer)
        db.session.commit()
        flash("Question set added!")
        return(redirect(url_for('admin')))
    return(render_template('admin-addset.html', form=form))

@app.route('/admin/deletequestionset', methods=["GET", "POST"])
@login_required
def admin_deleteset():
    if(current_user.is_admin() == False):
        return "Access Denied"

    form=DeleteQuestionSetForm()
    if form.validate_on_submit():
        #check if no input entered or both. If either case raise error
        q_id = form.question_id.data
        q_text = form.question_text.data
        if not (q_id or q_text):
            flash("Error: Please enter some input")
            return render_template("admin-deleteset.html", form=form)
        elif q_id and q_text:
            flash("Error: Only one field may contain data")
            return render_template("admin-deleteset.html", form=form)
        
        #find corresponding question and delete from question table. Also delete relation from Questionanswer table. If cannot find return error.
        if q_id:
            present = db.session.query(Question.id).filter_by(id=form.question_id.data).scalar() is not None
            if not present:
                flash("Error: Could not find a question corresponding to the entered ID.")
                return render_template("admin-deleteset.html", form=form)
            else:
                if form.confirm.data == True:
                    QuestionAnswer.query.filter_by(question_id=form.question_id.data).delete()
                    Question.query.filter_by(id=form.question_id.data).delete()
                else:
                    flash("Error: Check confirm to delete the question")
                    return render_template("admin-deleteset.html", form=form)
        else:
            present=db.session.query(Question.id).filter_by(question=form.question_text.data).scalar() is not None
            if not present:
                flash("Error: Could not find question.")
                return render_template("admin-deleteset.html", form=form)
            else:
                if form.confirm.data == True:

                    question = Question.query.filter_by(question=form.question_text.data).first()
                    QuestionAnswer.query.filter_by(question_id=question.id).delete()
                    Question.query.filter_by(question=form.question_text.data).delete()
                else:
                    flash("Error: Check confirm to delete the question")
                    return render_template("admin-deleteset.html", form=form)
        db.session.commit()
        flash("Question set succesfully deleted")
        return redirect(url_for("admin"))
    return render_template("admin-deleteset.html",form=form)


@app.route('/admin/admin-stats', methods=["GET", "POST"])
@login_required
def admin_viewstats():
    if (current_user.is_admin() == False):
        return "Access Denied"
    
    cat = db.session.query(Quiz.category,Quiz.total_score,Quiz.attempts).order_by(func.sum(Quiz.total_score)).group_by(Quiz.category)
    #questions = Question.query.all()
    questions = Question.query.order_by(Question.category)
    return render_template("admin-stats.html", Cats=cat, Questions = questions)



@app.route('/admin/viewstats', methods=["GET", "POST"])
@login_required
def admin_viewuserstats():
    if (current_user.is_admin() == False):
        return "Access Denied"
    
    usersscore = db.session.query(Quiz,User).filter(User.id == Quiz.user_id).with_entities(Quiz.category,Quiz.attempts,Quiz.total_score,User.username)
    return render_template("viewstats.html", Cats=usersscore)

#quiz content
@app.route('/category', methods = ['GET', 'POST'])
def category():
    c = []
    for value in Question.query.distinct(Question.category):
        v = (str(value.category),str(value.category))
        if v in c:
            continue
        else:
            tup = tuple(v)
            c.append(tup)

    form = CategoryForm()
    form.categories.choices = c
    result = form.categories.data

    if form.is_submitted():
        if result != None:
            flash(result)
            x = Question.query.filter_by(category = result).order_by(func.random()).limit(10)
            q = []
            full_request = []
            t =[]
            answers = []
            correct =[]
            for i in x:
                q.append(str(i.question))
                ans = QuestionAnswer.query.filter_by(question_id = i.id)
                answers = []
                for j in ans:
                    sel = Answer.query.filter_by(id = j.answer_id).all()
                    if(j.correct == True):
                        correct.append(sel[0].answer)
                    answers.append(sel[0].answer)
                full_request.append(answers)
        
            y = {
                "username": str(current_user.username),
                "category": str(result),
                "questions": q,
                "answers": full_request,
                "correct answer": correct
            }
            session['request'] = y
            return(redirect(url_for('quiz')))
        else:
            flash(result)
            return(render_template('category.html', form=form))
        
    return(render_template('category.html', form=form))

@app.route('/user/<username>', methods = ['GET', 'POST'])
@login_required
def user(username):
    form = SearchUserForm() 
    user = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        if db.session.query(exists().where(User.username == form.search.data)).scalar():
            user = User.query.filter_by(username=form.search.data).first()
        else:
            flash("User not found.")
            return render_template('user.html', user=user, form=form, stats=stats)
    y = User.query.filter_by(username = user.username).first()
    user_id = y.id
    stats = db.session.query(Quiz.category,Quiz.total_score,Quiz.attempts,Quiz.user_id).filter_by(user_id = user_id)

    return render_template('user.html', user=user, form=form, stats=stats)

@app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if db.session.query(exists().where(User.username == form.username.data)).scalar():
           flash("Username taken!")
           return render_template('edit_profile.html', title='Edit Profile',form=form)
        else:
            u = form.username.data
            bio = form.userbio.data
            if u:
                current_user.username = u
                db.session.commit()
            if bio:
                current_user.userbio = form.userbio.data
                db.session.commit()
            if not u and not bio:
                flash('No input added')
                return redirect(url_for('user',username = current_user.username))
            flash('Changes were updated!')
            return redirect(url_for('user', username = current_user.username))
    return render_template('edit_profile.html', title='Edit Profile',form=form)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    
    # Get the JSON from the server...
    # quizQuestions = request.json['questions']
    if request.method == 'POST':
        data = request.json
        return jsonify(data)

    question_set = session.get('request')

    questions = question_set["questions"]
    answers = question_set["answers"]
    corrAnswers = question_set["correct answer"]

    return render_template("quiz.html", title="Quiz",   questions=questions,
                                                        answers=answers,
                                                        corrAnswers=corrAnswers)
    

                            
