from flask import Flask,render_template,url_for,flash,redirect,request
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from form import LoginForm,DebitForm
from load_data import *
import load_data


app = Flask(__name__ ,template_folder='templates' , static_folder='static')
app.config['SECRET_KEY'] = '5791628bpowerb0b13ce0c676dfde280ba245'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1107'
app.config['MYSQL_DB']='bank'

mysql = MySQL(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def hello():
    return render_template('Main_home.html',title="Home page")

@app.route("/home")
def home():
    return render_template('home.html',title="Home page 2")

@app.route("/about")
def about():
    return render_template('about.html',title="About")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data in load_data.dbemails and load_data.dbpasswords[load_data.dbemails.index(form.email.data)]==form.password.data:
            login_user(User(load_data.dbcustomer_id[load_data.dbemails.index(form.email.data)]), remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if(next_page) else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('sign_up.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    user_data,bank_detail,employee_detail=load_data.request_User_detail(current_user.id)
    return render_template('account.html', title="Account",user_data=user_data,bank_detail=bank_detail,employee_detail=employee_detail)

@app.route("/debit", methods=['GET', 'POST'])
@login_required
def debit():
    form = DebitForm()
    if form.validate_on_submit():
        if form.Account_number.data=='ACC-101':
            return redirect(url_for('home'))
        else :
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('debit.html', title='Debit', form=form)

@app.route("/summary")
@login_required
def summary():
    summary = load_data.request_User_summary(current_user.id)
    return render_template('summary.html', title='Summary', user_data=load_data.request_User_detail_small(current_user.id))

if __name__ == '__main__':
    app.run(debug=True)