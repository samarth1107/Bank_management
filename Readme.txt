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
