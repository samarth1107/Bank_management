from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    Name = StringField('Username',validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    
    house_no = StringField('House No')

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DebitForm(FlaskForm):
    Account_number = StringField('Account Number', validators=[Regexp(regex=r'^ACC-\d{3}$',message="Example Account number ACC-101")])
    Pin = StringField('Pin Number', validators=[Length(min=4, max=4)])
    submit = SubmitField('Transfer')