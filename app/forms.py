from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class LoginForm(FlaskForm):
    nickname = StringField("Nickname", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField("Log in")


class SignupForm(LoginForm):
    email = StringField("Nickname", [validators.DataRequired()])
    submit = SubmitField("Sign up")

