from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, Required


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    houseno = StringField('House_no', validators=[DataRequired(), Length(min=1, max=50)])
    sector= StringField('Sector', validators=[DataRequired(), Length(min=3, max=20)])
    city = StringField('City', validators=[DataRequired(), Length(min=3, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=3, max=20)])
    pin = StringField('PinCode', validators=[DataRequired(), Length(min=6, max=6)])
    age = StringField('Age', validators=[DataRequired(), Regexp(regex=r'^[2-9][0-9]$|^1[0-9][0-9]$',message="Person above 19 age is allowed")])
    gender = StringField('Gender', validators=[DataRequired(), Regexp(regex=r'^[MFO]$',message="Valid inputs are 'M' for male 'F' for female or 'O' for others")])
    dob = StringField('Date Of Birth', validators=[DataRequired(), Required()])
    father = StringField('Fathers Name', validators=[DataRequired(), Length(min=3, max=20)])
    mother = StringField('Mothers Name', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Bank_LoginForm(FlaskForm):
    bank_id = StringField('BANK ID',validators=[DataRequired(), Regexp(regex=r'^BANK\d{6}$',message="Bank ID should be in the form of BANK100001")])
    branch_id = StringField('Branch ID',validators=[DataRequired(), Length(min=6,max=6)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default="unchecked")
    submit = SubmitField('Login')

class DebitForm(FlaskForm):
    Account_number = StringField('Account Number', validators=[Regexp(regex=r'^ACC-\d{3}$',message="Example Account number ACC-101")])
    Pin = StringField('Pin Number', validators=[Length(min=4, max=4)])
    Amount = StringField('Amount', validators=[Length(min=0, max=15)])
    submit = SubmitField('Transfer')

class Loan_enquiryForm(FlaskForm):
    principal = IntegerField('Loan Amount')
    max_period = IntegerField('Period (Enter in months')
    loan_type = SelectField('Type', choices=[('Car','Car'),('Home','Home'),('Business','Business'),('Personal','Personal'),('Extra','Extra')])
    submit = SubmitField('Enquire')