from Main import mysql,app
from flask_login import UserMixin
import itertools
from datetime import datetime

#This is for user class
class User(UserMixin):

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}', '{self.name}', '{self.account_no}', '{self.balance}', '{self.PIN}')"

    def __init__(self, id):
        user_data,bank_detail,employee_detail = request_User_detail(id)
        self.id = id
        self.email = user_data['email']        
        self.name = user_data['name']
        self.account_no = bank_detail['account_no']
        self.balance = bank_detail['account_balance']
        self.PIN = bank_detail['account_pin']

#This is for bank class
class Bank(UserMixin):
    def __repr__(self):
        return f"Bank('{self.id}', '{self.branch}', '{self.password}'"
    def __init__(self, id, branch, password):
        self.id=id
        self.branch=branch
        self.password=password

def Verify_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Customer_id,email,password FROM bank.customer_login_detail;")
    data = cur.fetchall()
    cur.close()
    dbemail = [sub['email'] for sub in data] 
    if email in dbemail:
        user_index = dbemail.index(email)
        dbpassword = [sub['password'] for sub in data] 
        if dbpassword[user_index]==password:
            dbcustomer_id = [sub['Customer_id'] for sub in data] 
            return dbcustomer_id[user_index]
        else:return -1
    else:return -1
    
def Verify_banker(bank_id, branch_id, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.bank_login_detail;")
    data = cur.fetchall()
    cur.close()
    
    bank_ids = [sub['Bank_id'] for sub in data] 
    branch_ids = [sub['Branch_id'] for sub in data] 
    dbpassword = [sub['password'] for sub in data] 
    
    a_index = bank_ids.index(bank_id)
    b_index = branch_ids.index(branch_id)
    c_index = dbpassword.index(password)

    if a_index==b_index and a_index==c_index:return 1
    else: return -1
        
def request_User_detail(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM bank.customer_personal_detail WHERE Customer_id = %s;",[int(id)])
    user_info = ((cur.fetchone()))

    cur.execute("SELECT * FROM bank.customer_bank_details WHERE customer_id = %s;",[int(id)])
    bank_detail = (cur.fetchone())

    cur.execute("SELECT * FROM bank.customer_employment_details WHERE Customer_id = %s;",[int(id)])
    employee_detail = (cur.fetchone())

    cur.close()

    return user_info,bank_detail,employee_detail

def request_User_detail_small(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.customer_personal_detail WHERE Customer_id = %s;",[int(id)])
    user_info = ((cur.fetchone()))
    cur.close()
    return user_info

def request_User_bank_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT bank_id,bank_name,account_no,account_balance,account_pin FROM bank.customer_bank_details WHERE Customer_id = %s;",[int(id)])
    bank_detail = (cur.fetchone())
    cur.close()
    return bank_detail

def Does_user_exist(acc_no):
    cur = mysql.connection.cursor()
    cur.execute("SELECT count(bank_id) FROM bank.customer_bank_details WHERE account_no = %s;",[str(acc_no)])
    bank_detail = int(cur.fetchone()['count(bank_id)'])
    cur.close()
    if (bank_detail)>0:return True
    else: return False

def make_transaction(acc_from,acc_to,amount):
    cur = mysql.connection.cursor()
    #Update users bank detail (balance)
    cur.execute("UPDATE bank.customer_bank_details SET account_balance = (account_balance - %s) WHERE account_no = %s;",[int(amount),str(acc_from)])
    update_user_summary(acc_from,amount,"Debited","Person")
    cur.execute("UPDATE bank.customer_bank_details SET account_balance = (account_balance + %s) WHERE account_no = %s;",[int(amount),str(acc_to)])
    update_user_summary(acc_to,amount,"Credited","Person")
    mysql.connection.commit()
    cur.close()  

def update_user_summary(account_no,amount,status,company):
    cur = mysql.connection.cursor()

    cur.execute("Select customer_id,account_balance FROM  bank.customer_bank_details WHERE account_no = %s;",[str(account_no)])
    info=(cur.fetchone())
    user_ID=int(info['customer_id'])
    balance=float(info['account_balance'])

    cur.execute("Select count(Serial_No) from bank.customer_account_summary where Customer_ID= %s;",[int(user_ID)])
    total_transaction=int((cur.fetchone())['count(Serial_No)'])

    cur.execute("INSERT into bank.customer_account_summary VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",[int(user_ID),int(total_transaction+1),str(status),str(company),float(amount),str(datetime.now().strftime("%Y-%m-%d")),str(datetime.now().strftime("%H:%M:%S")),float(balance)])
    mysql.connection.commit()
    cur.close()

def request_User_summary(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.customer_account_summary WHERE Customer_id = %s;",[int(id)])
    user_summary = cur.fetchall()
    cur.close()
    return user_summary
    
def insert_user(user_detail):
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(CUSTOMER_ID) FROM bank.customer_personal_detail")
    id_val = int(cur.fetchone()['MAX(CUSTOMER_ID)'])+1
    cur.execute("INSERT INTO bank.customer_personal_detail VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [id_val, user_detail[0], user_detail[1], user_detail[2], user_detail[3], user_detail[4], user_detail[5], user_detail[6], user_detail[7], user_detail[8], user_detail[9], user_detail[10], user_detail[11]])
    mysql.connection.commit()
    cur.close()

def enquire_loan(type,principal,period):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.bank_loan_detail WHERE loan_type=%s AND max_period>%s;",[str(type),int(period)])
    loan_details = cur.fetchall()
    cur.close()
    if len(loan_details)>0:
        EMI = []
        for loan in loan_details:
            interest = round((principal*loan['interest']*period)/100,2)
            total_amount=round(principal+interest,2)
            emi = round(total_amount/period,2)
            EMI.append([interest,total_amount,emi])
        data_loan = []
        for entry in loan_details:
            data_loan.append(list(entry.values()))
        return data_loan,EMI
    else: return False,False
    