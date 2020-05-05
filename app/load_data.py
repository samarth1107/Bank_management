from main import mysql,app
from flask_login import UserMixin
import itertools
from datetime import datetime

#This is for user class
class User(UserMixin):

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}', '{self.name}', '{self.bank_id}','{self.account_no}', '{self.balance}', '{self.PIN}', '{self.loan}', '{self.paid}')"

    def __init__(self, id):
        user_data,bank_detail,employee_detail = request_User_detail(id)
        self.id = id
        self.email = user_data['email']        
        self.name = user_data['name']
        self.bank_id = bank_detail['bank_id']
        self.account_no = bank_detail['account_no']
        self.balance = bank_detail['account_balance']
        self.PIN = bank_detail['account_pin']
        self.loan = 0
        self.paid = 0

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

#this is for corporate class
class Company(UserMixin):
    def __repr__(self):
        return f"Company('{self.id}', '{self.name}'"
    def __init__(self, id):
        data = request_Compnay_detail(id)
        self.id=data['comp_id']
        self.name=data['company_name']

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

def Verify_company(comp_id, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.company_login_detail;")
    data = cur.fetchall()
    cur.close()
        
    for row in range(len(data)):
        if data[row]['company_id']==comp_id:
            if (data[row]['password']==password):return 1
    else: return -1

def request_Compnay_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.company_market_detail;")
    data = cur.fetchone()
    cur.close()
    return data

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
    cur.execute("INSERT INTO bank.customer_personal_detail VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", [id_val, user_detail[0], user_detail[1], user_detail[2], user_detail[3], user_detail[4], user_detail[5], user_detail[6], user_detail[7], user_detail[8], user_detail[9], user_detail[10], user_detail[11]])
    mysql.connection.commit()
    cur.close()

def enquire_loan(type,principal,period, bank_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.bank_loan_detail WHERE loan_type=%s AND max_period>%s AND bank_id=%s;",[str(type),int(period),str(bank_id)])
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
    else: return False,
    
def insert_data_into_temporary_table(data,principal,max_period):
    cur = mysql.connection.cursor()
    for row in range(len(data)):
        cur.execute("INSERT INTO bank.loan_table VALUES(%s, %s, %s);",[data[row][0],principal,max_period])
        mysql.connection.commit()
    cur.close()
    return True

def apply_loan(Customer_id,loan_id):
    cur = mysql.connection.cursor()
    cur.execute("Select MAX(application_id) from bank.loan_application_data;")
    application = int(cur.fetchone()['MAX(application_id)'])+1
    cur.execute("Select * from bank.loan_table WHERE Loan_ID = %s;",[loan_id])
    data = cur.fetchone()
    cur.execute("Insert INTO bank.loan_application_data values(%s,%s,%s,'PENDING',%s,%s);",[int(application),int(loan_id),int(Customer_id),int(data['principal']),int(data['max_period'])])
    mysql.connection.commit()
    cur.execute("DELETE from bank.loan_table WHERE Loan_ID>0;")
    mysql.connection.commit()
    cur.execute("UPDATE bank.customer_bank_details SET loan_status = 'PENDING' WHERE (application_id = %s);",[(Customer_id)])
    cur.close()
    return

def delete_all_row():
    cur = mysql.connection.cursor()
    cur.execute("DELETE from bank.loan_table WHERE Loan_ID>0;")
    mysql.connection.commit()
    cur.close()
    return

def current_loan(Customer_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.loan_application_data l LEFT JOIN bank_loan_detail b ON l.Loan_id=b.loan_id WHERE l.Customer_id=%s;",[Customer_ID])
    data = cur.fetchall()
    cur.close()
    return data

def pay_emi_current_loan(user_id, application,account_no,bankid):
    cur = mysql.connection.cursor()
    data = current_loan(user_id)
    emi=0
    for loan in data:
        print(loan)
        if int(loan['application_id'])==int(application):
            emi=loan['principal']/loan['max_period']
            print(loan)
            break
        
    cur.execute("UPDATE bank.customer_bank_details SET account_balance = (account_balance - %s) WHERE account_no = %s;",[int(emi),str(account_no)])
    update_user_summary(account_no,emi,"Debited","EMI")
    mysql.connection.commit()

    cur.execute("SELECT total_assets FROM bank.bank WHERE bank_id=%s;",[str(bankid)])
    account_balance=cur.fetchone()['total_assets']
    cur.execute("UPDATE bank.bank SET total_assets = (%s) WHERE bank_id = %s;",[int(emi+account_balance),str(bankid)])
    mysql.connection.commit()   

    cur.execute("SELECT emi_paid FROM bank.loan_application_data WHERE application_id=%s;",[str(application)])
    emi_paid=cur.fetchone()['emi_paid']
    cur.execute("UPDATE bank.loan_application_data SET emi_paid = (%s) WHERE application_id = %s;",[int(emi_paid+1),str(application)])
    mysql.connection.commit()   

    cur.close()
    return True

def accept_loan(application_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT l.principal,l.max_period,b.interest,b.bank_id FROM bank.loan_application_data l LEFT JOIN bank.bank_loan_detail b ON l.Loan_id = b.loan_id WHERE l.application_id=%s;",[int(application_id)])
    details=cur.fetchone()
    interest_amount=(details['principal']*details['max_period']*details['interest'])/100
    cur.execute("UPDATE bank.loan_application_data SET Status = 'ACCEPTED', principal = %s, start_time=%s, emi_paid='0' WHERE (application_id = %s);",[int(details['principal']+interest_amount),str(datetime.now().strftime("%Y-%m-%d")),int(application_id)])
    mysql.connection.commit()

    cur.execute("SELECT total_assets FROM bank.bank WHERE bank_id=%s;",[str(details['bank_id'])])
    account_balance=cur.fetchone()['total_assets']
    cur.execute("UPDATE bank.bank SET total_assets = %s WHERE (bank_id = %s);",[int(account_balance-details['principal']),str(details['bank_id'])])
    cur.close()
    return True

def reject_loan(application_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE bank.loan_application_data SET Status = 'REJECTED' WHERE (application_id = %s);",[int(application_id)])
    mysql.connection.commit()
    cur.close()
    return True

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

def customers_loan_list(bankid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT s.customer_id,s.name,s.email,s.house_no,s.sector,s.city,s.city,s.state,s.pin_code,s.age,s.gender,s.dob,m.bank_id,m.account_no,m.account_balance,m.account_type,m.account_pin,d.password,l.application_id,l.Loan_id,l.start_time,l.emi_paid,l.Status FROM customer_personal_detail s LEFT JOIN customer_bank_details m ON s.customer_id = m.customer_id LEFT JOIN customer_login_detail d ON d.customer_id = m.customer_id LEFT JOIN loan_application_data l ON l.Customer_id = m.customer_id WHERE m.bank_id=%s AND l.status='ACCEPTED';",[str(bankid)])
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

def bank_recc(val):
    if val=="Most Trusted":
        cur = mysql.connection.cursor()
        cur.execute("SELECT bank_id, bank_name, branch_id, branch_name, branch_contact_number, number_of_customer, ROI_for_loans, ROI_for_savings, ROI_for_current, min_acc_balance from (select bank_id, bank_name, branch_id, branch_name, branch_contact_number, number_of_customer, ROI_for_loans, ROI_for_savings, ROI_for_current, min_acc_balance from bank.bank where annual_share_govt>20000) as t1 where number_of_customer > 200")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()

        return data

    elif val=="Loan Friendly":
        cur = mysql.connection.cursor()
        cur.execute("SELECT bank_id, bank_name, branch_id, branch_name, branch_contact_number, number_of_customer, ROI_for_loans, ROI_for_savings, ROI_for_current, min_acc_balance from bank.bank where ROI_for_loans <= (SELECT AVG(roi_for_loans) from bank.bank)")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()

        return data
    elif val=="Best for Savings":
        cur = mysql.connection.cursor()
        cur.execute("SELECT bank_id, bank_name, branch_id, branch_name, branch_contact_number, number_of_customer, ROI_for_loans, ROI_for_savings, ROI_for_current, min_acc_balance from bank.bank where ROI_for_savings >= (SELECT AVG(roi_for_savings) from bank.bank) and no_of_fds >=(select avg(no_of_fds) from bank.bank)")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return data
    elif val=="Least Minimum Account Balance":
        cur = mysql.connection.cursor()
        cur.execute("SELECT bank_id, bank_name, branch_id, branch_name, branch_contact_number, number_of_customer, ROI_for_loans, ROI_for_savings, ROI_for_current, min_acc_balance from bank.bank where min_acc_balance = (select min(min_acc_balance) from bank.bank)")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return data
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT bank_id, bank_name, branch_id, branch_name, branch_contact_number, number_of_customer, ROI_for_loans, ROI_for_savings, ROI_for_current, min_acc_balance from bank.bank")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return data

def load_market_data(para):
    data=0
    if para =="pe_ratio":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM bank.company_market_detail ORDER BY pe_ratio")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    if para =="market_value":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM bank.company_market_detail ORDER BY market_value")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    if para =="company_name":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM bank.company_market_detail ORDER BY company_name")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return data

def own_market_data(comp_id):
    cur = mysql.connection.cursor()
    cur.execute("select * from bank.company_market_detail where comp_id=%s",[comp_id])
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data     

def better_company(comp_id):
    cur = mysql.connection.cursor()
    cur.execute("select * from bank.company_market_detail where pe_ratio > (select pe_ratio from bank.company_market_detail where comp_id=%s) or eps > (select eps from bank.company_market_detail where comp_id=%s)",[comp_id,comp_id])
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data   

def rev_by_category():
    cur = mysql.connection.cursor()
    cur.execute("select category, sum(price*sold) as revenue from bank.products group by category")
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data   

def best_company():
    cur = mysql.connection.cursor()
    cur.execute("(select * from bank.company_market_detail where pe_ratio = (select max(pe_ratio) from company_market_detail)) union (select * from bank.company_market_detail where eps = (select max(eps) from company_market_detail))")
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data    

def load_employee_data(comp_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bank.customer_employment_details WHERE COMPANY_ID=(%s)", [comp_id])
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data

def load_su_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT su_id, su_name,account_id,date_created, sales_type, registered_email, linked_accounts, locations, size  FROM bank.startups")
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data

def custom_duty(comp_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT (raw_material + finished_product)*(custom_duty + gst - relaxation_limit)/100 FROM bank.company_imports WHERE COMP_ID=(%s)", [comp_id])
    data = cur.fetchall()
    cur.close()
    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data

def add_amount(id,amount,radio):
    if radio=="Employee":
        cur = mysql.connection.cursor()
        cur.execute("UPDATE bank.customer_bank_details SET account_balance = account_balance+%s WHERE customer_id = %s",[int(amount),id])
        mysql.connection.commit()
        cur.close()
    elif radio=="Start Ups":
        cur = mysql.connection.cursor()
        cur.execute("UPDATE bank.startups SET bank_balance = bank_balance+%s WHERE su_id = %s",[int(amount),id])
        mysql.connection.commit()
        cur.close()
    return True
    
def load_products(value):
    if value=='Books':
        cur = mysql.connection.cursor()
        cur.execute("SELECT seller_id, product_id,product_name,category,price FROM bank.products WHERE category=%s",['Books'])
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    elif value == 'Fashion':
        cur = mysql.connection.cursor()
        cur.execute("SELECT seller_id, product_id,product_name,category,price FROM bank.products WHERE category=%s",['Fashion'])
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    elif value == 'Health':
        cur = mysql.connection.cursor()
        cur.execute("SELECT seller_id, product_id,product_name,category,price FROM bank.products WHERE category=%s",['Health'])
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    elif value == 'Electronics':
        cur = mysql.connection.cursor()
        cur.execute("SELECT seller_id, product_id,product_name,category,price FROM bank.products WHERE category=%s",['Electronics'])
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    elif value == 'Lowest Prices':
        cur = mysql.connection.cursor()
        cur.execute("select f.seller_id, f.product_id,f.product_name,f.category,f.price from ( select category, min(price) as minprice from products group by category) as x inner join products as f on f.category = x.category and f.price = x.minprice")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    elif value == 'Best Sellers':
        cur = mysql.connection.cursor()
        cur.execute("select f.seller_id, f.product_id,f.product_name,f.category,f.price from ( select category, max(sold) as maxsold from products group by category) as x inner join products as f on f.category = x.category and f.sold = x.maxsold")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    elif value == 'graph':
        cur = mysql.connection.cursor()
        cur.execute("SELECT distinct(seller_id), product_id,product_name,category,(price*sold) as revenue FROM products order by seller_id")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close() 
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT seller_id, product_id,product_name,category,price FROM bank.products order by price")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()

    statements = []
    for entry in data:
        statements.append(list(entry.values()))
    data=statements
    return data
