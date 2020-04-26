from flask import Flask,render_template,url_for,flash,redirect,request
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from form import LoginForm, DebitForm, RegisterForm, Loan_enquiryForm, Bank_LoginForm, Search_customer, ADD_loan, submitbutton
from load_data import *
import load_data


app = Flask(__name__ ,template_folder='templates' , static_folder='static')
app.config['SECRET_KEY'] = '5791628bpowerb0b13ce0c676dfde280ba245'

app.config['MYSQL_HOST']='10.0.0.6'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1107'
app.config['MYSQL_DB']='bank'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


@login_manager.user_loader
def load_user(id):
    if len(id)==10:return User(id)
    if len(id)<10:return Bank(id)
    return None

@app.route("/")
def hello():
    return render_template('Main_home.html',title="Home page")

@app.route("/home")
def home():
    return render_template('home.html',title="Home page 2")

@app.route("/about")
def about():
    return render_template('about.html',title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_info = [form.name.data, form.email.data, form.houseno.data, form.sector.data, form.city.data, form.state.data, form.pin.data, form.age.data, form.gender.data, form.dob.data, form.father.data, form.mother.data]
        load_data.insert_user(user_info)
        flash('Your account has been created! You are now able to log in', 'success')
    return render_template('register.html', title='Register', form=form)

@app.route("/login/User", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        verify_user=Verify_user(form.email.data,form.password.data)
        if verify_user!=-1:
            if form.remember.data:login_user(User(verify_user), remember=True)
            else:login_user(User(verify_user),remember=False)
            next_page = request.args.get('next')
            flash('Logged in successfully', 'success')
            return redirect(next_page) if(next_page) else redirect(url_for('home'))
        else:flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('sign_in.html', title='Login', form=form)

@app.route("/login/bank", methods=['GET', 'POST'])
def bank_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Bank_LoginForm()

    if form.validate_on_submit():
        verify_banker=Verify_banker(form.universal_id.data,form.bank_id.data,int(form.branch_id.data),form.password.data)
        if verify_banker!=-1:
            if form.remember.data:login_user(Bank(form.universal_id.data), remember=True)
            else:login_user(Bank(form.universal_id.data), remember=False)
            flash('Logged in successfully', 'success')
            return redirect(url_for('bank_home'))
        else:flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('bank_sign_in.html', title='Login', form=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    user_data,bank_detail,employee_detail=load_data.request_User_detail(current_user.id)
    user_data=list(user_data.values())
    bank_detail=list(bank_detail.values())
    employee_detail=list(employee_detail.values())
    return render_template('account.html', title="Account",user_data=user_data,bank_detail=bank_detail,employee_detail=employee_detail)

@app.route("/debit", methods=['GET', 'POST'])
@login_required
def debit():
    form = DebitForm()
    curr_user_bank_detail=request_User_bank_detail(current_user.id)

    if form.validate_on_submit():
        if form.Account_number.data!=current_user.account_no and int(form.Pin.data)==current_user.PIN:
            if int(form.Amount.data)<current_user.balance:
                if Does_user_exist(form.Account_number.data):
                    amount=float(form.Amount.data)
                    make_transaction(current_user.account_no,form.Account_number.data,amount)
                    flash('Trasaction successful', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Please enter valid Account number','danger')
            else:
                flash('Amount Cannot be more than balance','danger')
        else :
            flash('Please check your account number and PIN code', 'danger')
    return render_template('debit.html', title='Debit', form=form, bank_detail=list(curr_user_bank_detail.values()))

@app.route("/summary")
@login_required
def summary():
    summary = load_data.request_User_summary(current_user.id)

    data = []
    for entry in summary:
        data.append(list(entry.values()))

    return render_template('summary.html', 
                            title='Summary',
                            user_id=current_user.id,
                            user_name=current_user.name,
                            bank_detail=list(load_data.request_User_bank_detail(current_user.id).values()), 
                            summary=data)

@app.route("/loan_enquire", methods=['GET', 'POST'])
@login_required
def loan_enquire():
    form = Loan_enquiryForm()
    if form.validate_on_submit():
        loan_data,emi_data=enquire_loan(form.loan_type.data,form.principal.data,form.max_period.data)
        if loan_data!=False:
            return render_template('loan_enquire_result.html', title='Loan Enquiry', loan_data=loan_data, emi_data=emi_data,loop=range(len(loan_data)) , loan_type=form.loan_type.data, principal=int(form.principal.data))
        else:
            flash('No Loan available for your requirement','success')
    return render_template('loan_enquire.html', title='Loan Enquiry', form=form) 

@app.route("/bank/home")
@login_required
def bank_home():
    return render_template('bank_home.html', title='Bank_home', total_customer=len(request_customerlist(current_user.bank_id,0,'customer_id')), pending_loan=len(search_loan_application('PENDING',current_user.bank_id)))

@app.route("/bank/customer", methods=['GET', 'POST'])
@login_required
def print_customer_list():
    form = Search_customer()
    if form.validate_on_submit():
        column=form.query_type.data
        term=form.query.data
        data=request_customerlist(current_user.bank_id,term,column)
        if data==None or len(data)==0:
            return render_template('customer_list.html', title='Customer list', customer_list=[], record=False, many_recored=False, form=form)
        else:
            if len(data)==1:
                summary = load_data.request_User_summary(data[0]['customer_id'])
                statements = []
                for entry in summary:
                    statements.append(list(entry.values()))
                return render_template('customer_list.html', title='Customer list', customer_list=data[0], record=True, many_recored=False, summary=statements,form=form)
            else:return render_template('customer_list.html', title='Customer list', customer_list=data, record=True, many_recored=True, form=form)
    customer_list=request_customerlist(current_user.bank_id,0,'customer_id')
    return render_template('customer_list.html', title='Customer list', customer_list=customer_list, record=True, many_recored=True, form=form)

@app.route("/bank/add_loan", methods=['GET', 'POST'])
@login_required
def add_loan():  
    current_loan=current_loan_in_database(current_user.bank_id,'0')
    form=ADD_loan()
    if form.validate_on_submit():
        insert_loan_in_database(current_user.bank_id,form.loan_type.data,form.interest.data,form.max_period.data)
        flash('New loan added into list','success')
        return redirect(url_for('bank_home'))
    return render_template('bank_add_loan.html',form=form, current_loan=current_loan)

@app.route("/bank/clear_loan", methods=['GET', 'POST'])
@login_required
def clear_loan():   
    applications = search_loan_application('PENDING',current_user.bank_id)
    if request.method=='POST':
        customer_list=request_customer_detail((request.form['submit']))
        print(customer_list)
        summary = load_data.request_User_summary(customer_list['customer_id'])
        statements = []
        for entry in summary:
            statements.append(list(entry.values()))
        return render_template('customer_detail.html', customer_list=customer_list, summary=statements) 
    else:
        if type(applications)==int:
            return render_template('bank_loan_applications.html', hasdata=False)
        else:
            return render_template('bank_loan_applications.html', hasdata=True, current_loan=applications)


if __name__ == '__main__':
    app.run(debug=True)