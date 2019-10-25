from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
     username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
     email = StringField('Email', validators=[DataRequired(), Email()])
     passowrd = PasswordField('Password', validators=[DataRequired()])
     confirm_passowrd = PasswordField('Confirm Password', validators=[DataRequired(), EaualTo('passowrd')])
     submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
     email = StringField('Email', validators=[DataRequired(), Email()])
     passowrd = PasswordField('Password', validators=[DataRequired()])
     remember_me = BooleanField("Remember Me")
     submit = SubmitField("Login")
