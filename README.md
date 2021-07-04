**Monergise**
The capital management system which will deal with management and transfer of digital currency and has the following stakeholders. 
This unique database management application can solve the problems of several categories of organisations at once. This system is a unified capital management system, one source for all kinds of financial services. 
Our Web-Application provides a centralized control to the government on all the Customers, Banks and Businesses.

*Home page*
![](screenshots/Home_page.png)    

*Customer (Citizem) home page*
![](screenshots/Customer.png)    

*Bank customer Home page*
![](screenshots/Bank.png)    

*Company home page*
![](screenshots/Company.png)


[You can check our weekly progress](Work in progress.pdf)
[You can check schema of DBMS of this project](Database Schema - Entity Relationship Diagram (UML Notation).png)


This is optimised for windows 10

To setup MySQL database (for MySQL workbench) 
1. login through your localhost server  
2. then go to server option in the option panel -> Data Import  
3. select Import from Dump project folder 
4. from 3 dot option select Database folder from our project  
5. click start import   
6. check if data is imported successfully

To enter password in file
1. Now open app/main.py 
2. search line with 'app.config['MYSQL_PASSWORD']' and change the password with your MySQL password
3. save the file

To run this project    
1. Open cmd or powershell in side the folder
2. flask_app/Scripts/activate
3. cd app 
4. python main.py


Troubleshoots : -   

there must be master key in the python file

(flask_mysqldb is not importing)
then download wheel file from the unofficial website


mysql80 service should be active other wise connection will not be done

(For error MySQLdb._exceptions.OperationalError: (2059, "Authentication plugin 'caching_sha2_password' cannot be loaded: The specified module could not be found.\r\n"))
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by '1107';
