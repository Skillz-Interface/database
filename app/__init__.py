from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST']= '0.0.0.0'
app.config['PORT']='8080'
app.config['MYSQL_USER']= 'skillxtemper'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] = 'recipeApp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['SECRET_KEY'] = "this is a super secure key"

#init MYSQL


from app import views