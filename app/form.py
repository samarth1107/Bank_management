from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField
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
    universal_id = StringField('Universal ID', validators=[DataRequired(), Length(min=3, max=5)])
    bank_id = StringField('BANK ID',validators=[DataRequired(), Regexp(regex=r'^BANK\d{6}$',message="Bank ID should be in the form of BANK100001")])
    branch_id = StringField('Branch ID',validators=[DataRequired(), Length(min=6,max=6)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3,max=45)])
    remember = BooleanField('Remember Me', default="unchecked")
    submit = SubmitField('Login')

class Company_LoginForm(FlaskForm):
    company_id = StringField('Company ID',validators=[DataRequired(), Regexp(regex=r'^COMP\d{6}$',message="Company ID should be in the form of COMP100001")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3,max=45)])
    remember = BooleanField('Remember Me', default="unchecked")
    submit = SubmitField('Login')

class DebitForm(FlaskForm):
    Account_number = StringField('Account Number', validators=[Regexp(regex=r'^ACC-\d{3}$',message="Example Account number ACC-101")])
    Pin = StringField('Pin Number', validators=[Length(min=4, max=4)])
    Amount = StringField('Amount', validators=[Length(min=0, max=15)])
    submit = SubmitField('Transfer')

class Loan_enquiryForm(FlaskForm):
    principal = IntegerField('Loan Amount')
    max_period = IntegerField('Period (Enter in months)')
    loan_type = SelectField('Type', choices=[('Car','Car'),('Home','Home'),('Business','Business'),('Personal','Personal'),('Extra','Extra')])
    submit = SubmitField('Enquire')

class Search_customer(FlaskForm):
    query = StringField('',validators=[Length(min=3)])
    query_type = SelectField('Type', choices=[('customer_id','ID'),('name','Name'),('email','Email'),('account_no','Account Number')])
    submit = SubmitField('Search')

class ADD_loan(FlaskForm):
    loan_type = SelectField('Type', choices=[('Car','Car'),('Home','Home'),('Business','Business'),('Personal','Personal'),('Extra','Extra')])
    interest = IntegerField('Interest in percentage')
    max_period = IntegerField('Period (Enter in months)')
    submit = SubmitField('Add Loan')

class submitbutton(FlaskForm):
    submit = SubmitField('Submit')

class BankPrefForm(FlaskForm):
    radio = RadioField('Parameters', choices=[('Most Trusted','Most Trusted'),('Loan Friendly','Loan Friendly'),('Best for Savings','Best for Savings'),('Least Minimum Account Balance','Least Minimum Account Balance'),('graph','Show Graphical Analysis')])
    submit = SubmitField('Search')

class StockForm(FlaskForm):
    radio = RadioField('Sort using:', choices = [('pe_ratio','Profit'),('market_value','Price'),('company_name','Name'),('graph1','Show PE Analysis'),('graph2','Show EPS Analysis')])
    submit = SubmitField('Search')

class PerformanceForm(FlaskForm):
    id = StringField('Company ID')
    submit = SubmitField('Submit')

class MNCPayForm(FlaskForm):
    id = StringField('Company ID')
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    id = StringField('Recipients ID')
    amount = StringField('Amount')
    radio = RadioField('Choose', choices=[('Employee','Employee'),('Start Ups','Start Ups')])
    cid = StringField('Your ID')
    pin = PasswordField('PIN')
    submit = SubmitField('CONFIRM')

class EKartForm(FlaskForm):
    radio = RadioField('Filters', choices=[('Health','Health'),('Fashion','Fashion'),('Books','Books'),('Electronics','Electronics'),('Best Sellers','Best Sellers'),('Lowest Prices','Lowest Prices'),('graph','Show Graphical Analysis')])
    submit = SubmitField('Find the right item!')

class Pay_EMI(FlaskForm):
    Pin = StringField('Pin Number', validators=[Length(min=4, max=4)])

class InvestForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    profession = StringField('Occupation', validators=[])
    profit = RadioField('How much return do you want?',choices=[('H','High'),('M','Medium'),('L','Low')])
    risk = RadioField('How risk can you take?',choices=[('H','High'),('M','Medium'),('L','Low')])
    time = RadioField('How much time can you invest?',choices=[('H','>5 Years'),('M','3-5 Years'),('L','0-3 Years')])
    capital = RadioField('How much capital can you invest?',choices=[('H','>10 Lakhs'),('M','1-10 Lakhs'),('L','<1 Lakhs')])
    submit = SubmitField('Find!')