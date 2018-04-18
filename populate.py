##import random
##import string
##def userRecords():
from app import app
import psycopg2
import traceback
from faker import Faker
from flask_mysqldb import MySQL
import mysql
mysql = MySQL(app)


fake = Faker()

def db_insert():
    
    
    try:
        print("Connecting to database")
        data_ = mysql.connect(database ="recipeApp",host="0.0.0.0",port="8080",user="skillxtemper",password="")
    except:
        print("Failed!!!")

    


	#conn = psycopg2.connect(database="testdb", user="****", password="****", host="127.0.0.1", port="5432")
	#print "Opened database successfully"
	cur = data_.cursor()

	for i in range (0,500000):
		
		userFname = fake.firstname()
		userLname = fake.lastname() 
		addressid =fake.random_int(min=1,max=100000)
		uPassword = fake.password(min_length = 6, max_length = 9)
		uPhoneNum = fake.phoneNumber()
		userAccName = fake.userName()
		uPrefferedMeal = fake.meal()
		
		cur.execute("INSERT INTO user (userAccName,userFname,userLname,uPassword,uPhoneNum,addressid,uPrefferedMeal) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)", (userAccName, userFname, userLname, uPassword,uPhoneNum,addressid,uPrefferedMeal));

	data_.commit()
	print ("Records created successfully")
	data_.close()
	
	
	
if __name__ == 'main':
	db_insert()
