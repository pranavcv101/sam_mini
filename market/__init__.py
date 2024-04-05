#the name __init__ is to make this market directory a package 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager#some lib for login stuff with database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
#secret key for forms
db = SQLAlchemy(app)
app.app_context().push()  #to avoid error when creating that database from terminal

bcrypt= Bcrypt(app)#for password encryption

login_manager = LoginManager(app)
login_manager.login_view = "login_page" #this is along with that login_required decorater  we used so that it takes u directly to login page if not logged in 
login_manager.login_message_category = "info" #this is for a flash message

#below code refer 2.0.0
from market import routes
from market import models