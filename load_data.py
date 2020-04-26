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
        return f"Bank('{self.id}', '{self.bank_id}', '{self.name}', '{self.branch}'"
    def __init__(self, id):
        data = request_Bank_detail(id)
        self.id=data['Universal_id']
        self.bank_id=data['bank_id']
        self.name=data['bank_name']
        self.branch=data['branch_id']

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
    
def Verify_banker(universal_id, bank_id, branch_id, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.bank_login_detail;")
    data = cur.fetchall()
    cur.close()
        
    for row in range(len(data)):
        if data[row]['Universal_id']==universal_id:
            if (data[row]['Bank_id']==bank_id and data[row]['Branch_id']==branch_id and data[row]['password']==password):
                return 1
    else: return -1

def request_Bank_detail(universal_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.bank WHERE Universal_id = %s;",[str(universal_id)])
    data = cur.fetchone()
    cur.close()
    return data
        
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

def request_customerlist(bankid, term, column):
    cur = mysql.connection.cursor()
    if term==0:
        cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id WHERE m.bank_id=%s;",[str(bankid)])
        customerlist=cur.fetchall()
        cur.close()
        return customerlist
    else:
        if column=='customer_id':
            cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id WHERE m.bank_id=%s AND s.customer_id LIKE %s;",[str(bankid),'%'+str(term)+"%"])
        elif column=='name':
            cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id WHERE m.bank_id=%s AND s.name LIKE %s;",[str(bankid),'%'+str(term)+'%'])
        elif column=='email':
            cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id WHERE m.bank_id=%s AND s.email LIKE %s;",[str(bankid),'%'+str(term)+'%'])
        else:
            cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id WHERE m.bank_id=%s AND m.account_no LIKE %s;",[str(bankid),'%'+str(term)+'%'])
        customerlist=cur.fetchall()
        cur.close()
        return customerlist

def current_loan_in_database(bank_id, loan_type):
    cur = mysql.connection.cursor()
    if loan_type=='0':
        cur.execute("SELECT * FROM bank.bank_loan_detail WHERE bank_id=%s;",[str(bank_id)])
        loans=cur.fetchall()
        cur.close()
        if loans==None or len(loans)==0:return -1
        else:return loans
    elif bank_id=='0' and loan_type=='0':
        cur.execute("SELECT * FROM bank.bank_loan_detail;")
        loans=cur.fetchall()
        cur.close()
        if loans==None or len(loans)==0:
            return -1
        else:return loans
    else:
        cur.execute("SELECT * FROM bank.bank_loan_detail WHERE bank_id=%s AND loan_type=%s;",[str(bank_id),str(loan_type)])
        loans=cur.fetchall()
        cur.close()
        if loans==None or len(loans)==0:
            return -1
        else:return loans

def insert_loan_in_database(bank_id, loan_type, interest, max_period):
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(loan_id) FROM bank.bank_loan_detail;")
    id_val = int(cur.fetchone()['MAX(loan_id)'])+1
    cur.execute("INSERT INTO bank.bank_loan_detail VALUES(%s, %s, %s, %s, %s)", [id_val, str(bank_id), str(loan_type), int(interest), int(max_period)])
    mysql.connection.commit()
    cur.close()

def search_loan_application(status, bank_id):
    cur = mysql.connection.cursor()
    if status=='0':
        cur.execute("SELECT * FROM bank.loan_application_data l LEFT JOIN bank.customer_bank_details b ON l.Customer_id=b.customer_id WHERE b.bank_id=%s;",[str(bank_id)])
        loans=cur.fetchall()
        cur.close()
        if loans==None or len(loans)==0:return -1
        else:return loans
    else:
        cur.execute("SELECT * FROM bank.loan_application_data l LEFT JOIN bank.customer_bank_details b ON l.Customer_id=b.customer_id WHERE b.bank_id=%s AND l.status=%s;",[str(bank_id),str(status)])
        loans=cur.fetchall()
        cur.close()
        if loans==None or len(loans)==0:
            return -1
        else:return loans


def request_customer_detail(term):
    cur = mysql.connection.cursor()
    cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password,e.Company_ID,e.Company_Name,e.Sector,e.Working_From,e.Working_Till FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id LEFT JOIN customer_employment_details e ON e.customer_id = s.customer_id WHERE s.customer_id LIKE %s;",['%'+str(term)+"%"])
    customerlist=cur.fetchone()
    cur.close()
    return customerlist