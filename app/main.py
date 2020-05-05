from flask import Flask,render_template,url_for,flash,redirect,request
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from form import *
from load_data import *
import pyqrcode 
import png 
from pyqrcode import QRCode
import re
import os
import pygal


app = Flask(__name__ ,template_folder='templates' , static_folder='static')
app.config['SECRET_KEY'] = '5791628bpowerb0b13ce0c676dfde280ba245'

app.config['MYSQL_HOST']='localhost'
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
    if 'COMP' in id:return Company(id)
    if 'B' in id:return Bank(id)
    if len(id)==10:return User(id)
    return None

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = InvestForm()
    if form.validate_on_submit():
        print(form.profit.data)
        if form.profit.data == 'H' and form.risk.data == 'L' and form.time.data == 'H':
            return redirect(url_for('nps'))                
        elif form.profit.data == 'M' and form.risk.data == 'L':
            return redirect(url_for('gold'))
        elif form.profit.data == 'H' and form.risk.data == 'H':
            return redirect(url_for('nifty'))
        elif form.profit.data == 'M' and form.risk.data == 'H':
            return redirect(url_for('sensex'))
        elif form.profit.data == 'H' and form.risk.data == 'M':
            return redirect(url_for('mutual'))
        elif form.profit.data == 'H' and form.risk.data == 'L' and form.time.data == 'L' and form.capital.data =='H':
            return redirect(url_for('real'))
        elif form.profit.data == 'M' and form.risk.data == 'L' and form.time.data == 'H':
            return redirect(url_for('ppf'))
        elif form.profit.data == 'L' and form.risk.data == 'L' and form.time.data == 'H':
            return redirect(url_for('fd'))
        elif form.profit.data == 'M' and form.risk.data == 'M':
            return redirect(url_for('bonds'))
        else:
            flash("Your requirements need to be modified for the accurate results",'success')
    return render_template('Main_home.html',title="Home page", form=form)

@app.route('/nps', methods=['GET', 'POST'])
def nps():
    return render_template('nps.html', title = 'NPS')

@app.route('/fd', methods=['GET', 'POST'])
def fd():
    return render_template('fd.html', title = 'NPS')

@app.route('/gold', methods=['GET', 'POST'])
def gold():
    return render_template('gold.html', title = 'NPS')

@app.route('/sensex', methods=['GET', 'POST'])
def sensex():
    return render_template('sensex.html', title = 'NPS')

@app.route('/nifty', methods=['GET', 'POST'])
def nifty():
    return render_template('nifty.html', title = 'NPS')

@app.route('/real', methods=['GET', 'POST'])
def real():
    return render_template('real.html', title = 'NPS')

@app.route('/ppf', methods=['GET', 'POST'])
def ppf():
    return render_template('ppf.html', title = 'NPS')

@app.route('/mutual', methods=['GET', 'POST'])
def mutual():
    return render_template('mutual.html', title = 'NPS')

@app.route('/bonds', methods=['GET', 'POST'])
def bonds():
    return render_template('bonds.html', title = 'NPS')

@app.route("/home")
@login_required
def home():
    data = current_loan(current_user.id)
    if len(data)>0:
        for loans in data:
            if loans['Status']=='ACCEPTED':
                loans['Status']=True
                current_user.loan = 1
                if datetime.now().day>25:
                    current_user.paid=True
    return render_template('home.html',title="Home page",loan=len(data))

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
        insert_user(user_info)
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
            url = pyqrcode.create("http://127.0.0.1:5000/debit/"+current_user.account_no) 
            url.png('static/css/myqr.png', scale = 6)
            flash('Logged in successfully', 'success')
            return redirect(next_page) if(next_page) else redirect(url_for('home'))
        else:flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('sign_in.html', user='Customer', form=form)

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

    return render_template('bank_sign_in.html', user='Bank', form=form)
    
@app.route("/login/company", methods=['GET', 'POST'])
def company_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Company_LoginForm()

    if form.validate_on_submit():
        verify_comp=Verify_company(form.company_id.data,form.password.data)
        if verify_comp!=-1:
            if form.remember.data:login_user(Company(form.company_id.data), remember=True)
            else:login_user(Company(form.company_id.data), remember=False)
            flash('Logged in successfully', 'success')
            return redirect(url_for('company_home'))
        else:flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('company_sign_in.html', user='Corporate', form=form)

@app.route("/logout")
def logout():
    logout_user()
    try:
        os.remove("static/css/myqr.png")
    except:
        pass
    return redirect(url_for('hello'))

@app.route("/account")
@login_required
def account():
    user_data,bank_detail,employee_detail= request_User_detail(current_user.id)
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

@app.route("/debit/<path:filename>", methods=['GET', 'POST'])
@login_required
def qr_debit(filename):
    form = DebitForm()
    if request.method=='POST':
        if filename!=current_user.account_no and int(form.Pin.data)==current_user.PIN:
            if int(form.Amount.data)<current_user.balance:
                if Does_user_exist(filename):
                    amount=float(form.Amount.data)
                    make_transaction(current_user.account_no,filename,amount)
                    flash('Trasaction successful', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Please enter valid Account number','danger')
            else:
                flash('Amount Cannot be more than balance','danger')
        else :
            flash('Please check your account number and PIN code', 'danger')
    if current_user.account_no in filename:
        return render_template('404.html',message='You cannot send money to yourself')
    pattern = re.compile("^ACC-\d{3}$")
    if pattern.match(filename) and Does_user_exist(filename):
        curr_user_bank_detail=request_User_bank_detail(current_user.id)
        return render_template('debit_dynamic.html', title='Debit', form=form,sender=filename ,bank_detail=list(curr_user_bank_detail.values()))
    else:
        return render_template('404.html',message='User with this account number not exist')

@app.route("/summary")
@login_required
def summary():
    summary =  request_User_summary(current_user.id)

    data = []
    for entry in summary:
        data.append(list(entry.values()))

    return render_template('summary.html', 
                            title='Summary',
                            user_id=current_user.id,
                            user_name=current_user.name,
                            bank_detail=list(request_User_bank_detail(current_user.id).values()), 
                            summary=data)

@app.route("/loan_enquire", methods=['GET', 'POST'])
@login_required
def loan_enquire():
    form = Loan_enquiryForm()
    delete_all_row()
    if request.method=='POST':
        if 'Apply for loan ID' in request.form['submit']:
            apply_loan(current_user.id,request.form['submit'][18:])
            flash('Your application is successfully submit to bank','success')
            return redirect(url_for('home'))
        if 'Search' in request.form['submit']:
            principal = form.principal.data
            max_period = form.max_period.data
            loan_data,emi_data=enquire_loan(form.loan_type.data,form.principal.data,form.max_period.data,current_user.bank_id)
            if loan_data!=False:
                insert_data_into_temporary_table(loan_data,form.principal.data,form.max_period.data)
                return render_template('loan_enquire.html', title='Loan Enquiry',enquire=False ,loan_data=loan_data, emi_data=emi_data,loop=range(len(loan_data)) , loan_type=form.loan_type.data, principal=int(form.principal.data), form=form)
            else:
                flash('No Loan available for your requirement','success')

    return render_template('loan_enquire.html', title='Loan Enquiry', form=form, request=True, enquire=True) 
    
@app.route("/loan", methods=['GET', 'POST'])
@login_required
def current_loans():
    data=current_loan(current_user.id)
    if request.method=='POST':
        form=Pay_EMI()
        if 'Pay EMI' in request.form['submit']:
            data=current_loan(current_user.id)
            for loan in data:
                if loan['application_id']==int(request.form['submit'][8:]):
                    emi = loan['principal']/loan['max_period']
                    if emi<current_user.balance:
                        return render_template('loans.html',payemi=False,loan=loan,form=form,title='Pay EMI',emi=emi)
                    else: 
                        flash('sufficient balance not available','danger')
                        return redirect(url_for('home'))
        if '_Pay_' in request.form['submit']:
            if int(form.Pin.data)!=int(current_user.PIN):
                flash('Incorrect PIN was entered','danger')
                return redirect(url_for('home'))
            else:
                pay_emi_current_loan(current_user.id,request.form['submit'][6:],current_user.account_no,current_user.bank_id)
                flash('Emi paid sucessfully','success')
                return redirect(url_for('home'))
    if len(data)>0:
        for loans in data:
            if loans['Status']=='ACCEPTED':
                loans['Status']=True
        return render_template('loans.html',payemi=True,data=data,manydata=True, title='Current Loan')
    else: return render_template('loans.html',payemi=True,manydata=False, title='Current Loan')

@app.route("/loan_remainder", methods=['GET', 'POST'])
@login_required
def emi_remainder():
    return redirect(url_for('current_loans'))

@app.route("/bank/home")
@login_required
def bank_home():
    loans_customer=search_loan_application('PENDING',current_user.bank_id)
    if loans_customer!=-1:pending_length=len(loans_customer)
    else: pending_length=0
    return render_template('bank_home.html', title='Bank home', total_customer=len(request_customerlist(current_user.bank_id,0,'customer_id')), pending_loan=pending_length)

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
                summary =  request_User_summary(data[0]['customer_id'])
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
        if 'Accept' in request.form['submit'] or 'Reject' in request.form['submit']:
            if 'Accept' in request.form['submit']:
                accept_loan(request.form['submit'][7:])
                flash('Loan application accepted','success')
                return redirect(url_for('bank_home'))
            else:
                reject_loan(request.form['submit'][7:])
                flash('Loan application rejected','success')
                return redirect(url_for('bank_home'))
        customer_list=request_customer_detail((request.form['submit']))
        summary =  request_User_summary(customer_list['customer_id'])
        statements = []
        for entry in summary:
            statements.append(list(entry.values()))
        return render_template('customer_detail.html',show_cust=True, customer_list=customer_list, summary=statements, loan_application_number=request.form['submit']) 
    else:
        if type(applications)==int:
            return render_template('customer_detail.html', show_cust=False, hasdata=False)
        else:
            return render_template('customer_detail.html', show_cust=False, hasdata=True, current_loan=applications)

# @app.route("/bank/loan/customer", methods=['GET', 'POST'])
# @login_required
# def current_loan_takers():
#     form = Search_customer()
#     customer_list = customers_loan_list(current_user.bank_id)
#     return render_template('customer_loan_list.html', title='Current customer list', customer_list = customer_list, form = form, many_record=True)

@app.route("/corporate/home", methods=['GET', 'POST'])
@login_required
def company_home():
    return render_template('company_home.html',title='Home')

@app.route("/banks/comparision", methods=['GET', 'POST'])
@login_required
def banks_performance():
    data =  bank_recc(0)
    form = BankPrefForm()
    if form.validate_on_submit():
        if(form.radio.data=='graph'):
            data=bank_recc('graph')
            print(data)
            bar_labels=[]
            bar_values=[]
            for j in data:
                bar_labels.append(j['bank_name'])
                bar_values.append(j['ROI_for_loans'])
            chart = pygal.Bar(width=1200, height=700,spacing=100,explicit_size=True)
            chart.title='ROI for Loan Comparison'
            for i in range(len(bar_labels)):
                chart.add(bar_labels[i],(bar_values[i]))
            graph = chart.render_data_uri()
            return render_template('Bank_performance.html', form=form, data=data, title='Bank Performance',show_graph=True,graph=graph)
        data = bank_recc(form.radio.data)
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return render_template('Bank_performance.html', form=form, data=data, title='Bank Performance',show_graph=False)

@app.route("/stock", methods=['GET', 'POST'])
@login_required
def stock_comparision():
    data = load_market_data('company_name')
    form = StockForm()
    if form.validate_on_submit():
        data = load_market_data('company_name')
        if(form.radio.data=='graph1'):
            data=load_market_data('company_name')
            bar_labels=[]
            bar_values=[]
            for j in data:
                bar_labels.append(j['company_name'])
                bar_values.append(j['pe_ratio'])
            chart = pygal.Bar(width=1200, height=700,spacing=100,explicit_size=True)
            chart.title='Price-to-Earnings Ratio Comparison'            
            for i in range(len(bar_labels)):
                chart.add(bar_labels[i],(bar_values[i]))
            graph = chart.render_data_uri()
            return render_template('stock_performance.html', form=form, data=data, bar_graph=True, graph=graph, title="Live Stocks")
        elif(form.radio.data=='graph2'):
            data=load_market_data('company_name')
            bar_labels=[]
            bar_values=[]
            for j in data:
                bar_labels.append(j['company_name'])
                bar_values.append(j['eps'])
            chart = pygal.Bar(width=1200, height=700,spacing=100,explicit_size=True)
            chart.title='Earnings-per-Share Ratio Comparison'
            for i in range(len(bar_labels)):
                chart.add(bar_labels[i],(bar_values[i]))
            graph = chart.render_data_uri()
            return render_template('stock_performance.html', form=form, data=data, bar_graph=True, graph=graph, title="Live Stocks")
        else:
            data = load_market_data(form.radio.data)
            statements = []
            for entry in data:
                statements.append(list(entry.values()))
                data=statements
            return render_template('stock_performance.html', form=form, data=data, bar_graph=False, title="Live Stocks")
    return render_template('stock_performance.html', form=form, data=data, bar_graph=False, title="Live Stocks")


@app.route("/corporate/perform", methods=['GET', 'POST'])
@login_required
def company_performance():
    data0 = (('NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'),)
    data = (('NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'),)
    data1 = (('NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'),)
    data2 = (('NA','NA'),)
    form = PerformanceForm()
    if form.validate_on_submit():
        data0 =  own_market_data(form.id.data)
        data = best_company()
        data1 =  better_company(form.id.data)
        data2 =  rev_by_category()
    return render_template('corporate_performance.html', form=form, data=data, data1=data1, data2 = data2, data0=data0, title='Performance')

@app.route("/coporate/mnc/pay", methods=['GET', 'POST'])
@login_required
def mnc_pay():
    data = (('NA','NA','NA','NA','NA','NA','NA'),)
    data1 = (('NA','NA','NA','NA','NA','NA','NA','NA'),)
    data2 = (('NA',),)
    form = MNCPayForm()
    if form.validate_on_submit():
        data = load_employee_data(form.id.data)
        data1 =  load_su_data()
        data2 =  custom_duty(form.id.data)
    return render_template('mnc_payment.html', form=form, data=data, data1=data1, data2 = data2, title='MNC Payment')

@app.route("/coporate/payment", methods=['GET', 'POST'])
@login_required
def corporate_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        id = form.id.data
        amount = form.amount.data
        radio = form.radio.data
        add_amount(id,amount,radio)
        flash("amount: "+amount+" transferred to "+radio+" "+id+" successfully "+' Transaction ID: 123456789')
    return render_template('corporate_payment.html', form=form, title='Corporate payments')

@app.route("/corporate/ekart", methods=['GET', 'POST'])
@login_required
def ekart():
    data = load_products(0)
    form = EKartForm()
    if form.validate_on_submit():
        if(form.radio.data=='graph'):
            data=load_products('graph')
            bar_labels=[]
            bar_values=[]
            for j in data:
                bar_labels.append(j[0])
                bar_values.append(j[4])
            chart = pygal.Bar(width=1200, height=700,spacing=100,explicit_size=True)
            chart.title='Comparison Based on Revenue'
            for i in range(len(bar_labels)):
                chart.add(bar_labels[i],(bar_values[i]))
            graph = chart.render_data_uri()
            return render_template('corporate_ekart.html', form=form, data=data, title='Ekart',show_graph=True, graph = graph)
        data =load_products(form.radio.data)
    return render_template('corporate_ekart.html', form=form, data=data, title='Ekart',show_graph=False)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)