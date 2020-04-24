from Main import mysql,app
from flask_login import UserMixin
import itertools
from datetime import datetime

with app.app_context():
    ###### User details
    cur = mysql.connection.cursor()

    cur.execute("SELECT Customer_id FROM bank.customer_login_detail;")
    dbcustomer_id = list(map(lambda x: x[0], (cur.fetchall())))

    cur.execute("SELECT email FROM bank.customer_login_detail;")
    dbemails = list(map(lambda x: x[0], (cur.fetchall())))

    cur.execute("SELECT password FROM bank.customer_login_detail;")
    dbpasswords = list(map(lambda x: x[0], (cur.fetchall())))

    cur.close()
    #######

#This is for user class
class User(UserMixin):

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}', '{self.name}', '{self.account_no}', '{self.balance}', '{self.PIN}')"

    def __init__(self, id):
        self.id = id
        self.email = dbemails[dbcustomer_id.index(int(id))]
        user_data,bank_detail,employee_detail = request_User_detail(id)
        self.name = user_data[1]
        self.account_no = bank_detail[3]
        self.balance = bank_detail[4]
        self.PIN = bank_detail[6]

def request_User_detail(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM bank.customer_personal_detail WHERE Customer_id = %s;",[int(id),])
    user_info = ((cur.fetchall()))

    cur.execute("SELECT * FROM bank.customer_bank_details WHERE customer_id = %s;",[int(id)])
    bank_detail = (cur.fetchall())

    cur.execute("SELECT * FROM bank.customer_employment_details WHERE Customer_id = %s;",[int(id)])
    employee_detail = (cur.fetchall())

    cur.close()

    user_info=list(itertools.chain(*user_info))
    bank_detail=list(itertools.chain(*bank_detail))
    employee_detail=list(itertools.chain(*employee_detail))

    return user_info,bank_detail,employee_detail

def request_User_detail_small(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.customer_personal_detail WHERE Customer_id = %s;",[int(id),])
    user_info = ((cur.fetchall()))
    cur.close()
    user_info=list(itertools.chain(*user_info))
    return user_info

def request_User_bank_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT bank_id,bank_name,account_no,account_balance,account_pin FROM bank.customer_bank_details WHERE Customer_id = %s;",[int(id)])
    bank_detail = (cur.fetchall())
    cur.close()
    bank_detail=list(itertools.chain(*bank_detail))
    return bank_detail

def Does_user_exist(acc_no):
    cur = mysql.connection.cursor()
    cur.execute("SELECT bank_id FROM bank.customer_bank_details WHERE account_no = %s;",[str(acc_no)])
    bank_detail = (cur.fetchall())
    bank_detail=list(itertools.chain(*bank_detail))
    cur.close()
    if (len(bank_detail)>0):return True
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
    info=(cur.fetchall())
    info=list(itertools.chain(*info))
    user_ID=int(info[0])
    balance=float(info[1])

    cur.execute("Select count(Serial_No) from bank.customer_account_summary where Customer_ID= %s;",[int(user_ID)])
    total_transaction=int(cur.fetchone()[0])

    print([int(user_ID),int(total_transaction+1),str(status),str(company),float(amount),str(datetime.now().strftime("%Y-%m-%d")),str(datetime.now().strftime("%H:%M:%S")),float(balance)])
    cur.execute("INSERT into bank.customer_account_summary VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",[int(user_ID),int(total_transaction+1),str(status),str(company),float(amount),str(datetime.now().strftime("%Y-%m-%d")),str(datetime.now().strftime("%H:%M:%S")),float(balance)])
    mysql.connection.commit()
    cur.close()

def request_User_summary(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.customer_account_summary WHERE Customer_id = %s;",[int(id)])
    user_summary = list(map(list,cur.fetchall()))
    return user_summary
    cur.close()

def insert_user(user_detail):
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(CUSTOMER_ID) FROM bank.customer_personal_detail")
    id_val = map(lambda x: x[0], (cur.fetchall()))
    id_val = str(list(id_val)[0]+1)
    cur.execute("INSERT INTO bank.customer_personal_detail VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [id_val, user_detail[0], user_detail[1], user_detail[2], user_detail[3], user_detail[4], user_detail[5], user_detail[6], user_detail[7], user_detail[8], user_detail[9], user_detail[10], user_detail[11]])
    mysql.connection.commit()
    cur.close()