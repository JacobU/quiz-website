from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    email = StringField("Email Address", validators=[Email()])
    username = StringField("Enter a Username", validators=[InputRequired()]) # Need to check in database if username already exists!!!!!!
    password = PasswordField("Enter a Password", validators=[InputRequired(), Length(min=4, message="Passwords must contain at least 4 characters ")]) #Change to a regex matching some password policy!
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', message="Passwords do not match! ")])   
    submit = SubmitField("Register")
