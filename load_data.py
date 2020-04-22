from Main import mysql,app
from flask_login import UserMixin
import itertools

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
        return f"User('{self.id}', '{self.email}', '{self.password}')"

    def __init__(self, id):
        self.id = id
        self.email = dbemails[dbcustomer_id.index(int(id))]

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
    user_info=list(itertools.chain(*user_info))
    return user_info

def request_User_summary(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.customer_account_summary WHERE Customer_id = %s;",[int(id)])
    user_summary = list(map(list,cur.fetchall()))
    return user_summary
