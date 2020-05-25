from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Email, Length, Optional
from app.models import User, Question

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, message="Please enter a password!")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    email = StringField("Email Address", validators=[Email(), Length(max=128, message="Emails must be 128 characters or less" )])
    username = StringField("Enter a Username", validators=[InputRequired()]) # Need to check in database if username already exists!!!!!!
    password = PasswordField("Enter a Password", validators=[InputRequired(), Length(min=4, message="Passwords must contain at least 4 characters ")]) #Change to a regex matching some password policy!
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', message="Passwords do not match! ")])   
    submit = SubmitField("Register")
    #check if user already exists
    def check_user(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user != None:
            raise ValidationError("This username is already in use")

class AddUserForm(FlaskForm):
    username = StringField("Enter a Username", validators=[InputRequired()])
    password = PasswordField("Enter a Password", validators=[InputRequired(), Length(min=4, message="Passwords must contain at least 4 characters")]) #change to regex
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', message="Passwords do not match")])
    admin = BooleanField("Administrator Permissions")
    submit=SubmitField("Create User")

    def check_user(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user != None:
            raise ValidationError("This username is already in use")

class EditUserForm(FlaskForm):
    delete = BooleanField("Delete User?")
    old_username=StringField("Enter user's current username")
    new_username=StringField("Enter a new username ")
    email=StringField("Enter a new email")
    password = PasswordField("Enter a new Password")
    password_confirm = PasswordField("Confirm Password", validators=[EqualTo("password", message="Passwords do not match")])
    admin = BooleanField("Keep/Grant Administrator Permissions:")
    submit=SubmitField("Apply Changes")

class CategoryForm(FlaskForm):
    categories = RadioField("Categories")
    submit=SubmitField('Start Quiz')

class AddQuestionSetForm(FlaskForm):
    existing_category = StringField("Enter an existing category name: ")
    new_category = StringField("Enter a new category name: ")
    question = StringField("Enter a question: ", validators=[InputRequired()])
    answer = StringField("Enter in the correct answer to the question: ", validators=[InputRequired()])
    fake_ans1 = StringField("Enter in the first false answer: ", validators=[InputRequired()])
    fake_ans2 = StringField("Enter in the second false answer: ", validators=[InputRequired()])
    fake_ans3 = StringField("Enter in the third false answer: ", validators=[InputRequired()])
    submit=SubmitField("Submit question set")

class DeleteQuestionSetForm(FlaskForm):
        question_id = StringField("Question-ID to delete: ")
        question_text = StringField("Enter the question to delete: ") 
        confirm = BooleanField("Confirm delete: ")
        submit = SubmitField("Delete question")
    
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators= [Optional()])
    userbio = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class SearchUserForm(FlaskForm):
    search = StringField("Search", validators=[InputRequired()])
    submit = SubmitField('Search')
