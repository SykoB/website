from flask import Flask, redirect, render_template, session, request, url_for, abort, flash, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from email.mime.text import MIMEText
from os import path
import os
import smtplib
import socket
from smtplib import SMTP
from datetime import date
import requests
import json










#VARIABLES-->

#FLASK

app = Flask(__name__)
x = Blueprint('users',__name__,template_folder='users')
app.register_blueprint(x)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = 'b\xdb\x87-\x00\x95\x19\r\xe5\xdf*\x99\xb0K\\\xb6\xf8\xb6PN\xf9\x90\xc0p\x90'
app.permanent_session_lifetime = timedelta(minutes=5)
#SQLALCHEMY
db = SQLAlchemy(app)
#LOGIN MANAGER
login_manager = LoginManager()
login_manager.login_view = 'user'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return users.query.get(int(id))


#DATABASE

class users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key="True")
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    password2 = db.Column(db.String(20), unique=True, nullable=False)
    pfp = db.Column(db.String(20), unique=True, nullable=False, default="default.jpg")
    notes = db.relationship('data')
    
   
    

def __init__(self, username, email, password,pfp,notes):
        self.username = username
        self.email = email
        self.password = password
        self.pfp = pfp
        self.notes = notes
       
class data(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    post = db.Column(db.String(400), unique=False, nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
   
    
    
    

def __init__(self, post, time,user_id):
    self.post = post
    self.time = time
    self.user_id = user_id
    

   
   


#ROUTES



@x.route('/users')
def x():
    return render_template('n.html')


@app.route('/')
def main():
        return render_template("main.html",user=current_user)








@app.route('/login/', methods=["POST","GET"])
def login():
        if request.method == "POST":
          
          username = request.form.get("username")
          password = request.form.get("password")
          
          
          print(request.form)
          user = users.query.filter_by(username=username).first()
          if user:
              if check_password_hash(user.password, password):
                  flash("Logged in mf", category="success")
                  login_user(user, remember=True)
                  print(user)
                  return redirect(url_for("user"))
              else:
                  flash("Password incorrect", category="error")
          else:
                  flash("User does not exist", category="error")
         
         
          
        return render_template("login.html",user=current_user)
        
   
        
        
    

        if "user" in session:
            session["user"] = user
            session.permanent = True
            flash("Already logged in!", category="error")
            return redirect(url_for("user"))
        
        

@app.route("/signup", methods=["POST", "GET"]) 
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get('password2')
        email = request.form.get("email")
        print(request.form)
       

        user = users.query.filter_by(email=email).first()
        
       
        
        
        if user:
            flash("User already exists!", category="error")
            
        elif len(email) < 7:
            flash("Email must be longer than 6 characters", category="error")
        elif len(username) < 4:
            flash("Username must be longer than 3 characters", category="error")
        elif len(password) < 4:
            flash("Password must be longer than 3 characters", category="error")
        elif password == password2:
            flash("Account created!", category="success")
            
            usr = users(email=email,username=username,password=generate_password_hash(password, method="sha256"),password2=password2)
            db.session.add(usr)
            db.session.commit()
            
           
           
            login_user(usr, remember=True)
            return redirect(url_for("user"))
    return render_template("signup.html",user=current_user)



@app.route('/recoveruser', methods=['POST','GET'])
def recover():
    
    if request.method == "POST":
        email = request.form.get('user')
        
        
        x = users.query.filter_by(email=email).first()
       
        
       
        if x:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login('k.dyakowski@gmail.com','huncwot24')
            server.ehlo()
           
            with open('templates/hello.html') as x:
                v = MIMEText(x.read(),'html')
                server.sendmail('k.dyakowski@gmail.com', email ,v.as_string())
            server.quit()
            flash('Check your email', category='success')
                
            
            
        else:
            flash('Email doesn\'t exist', category='error')
            
        
    return render_template('recover.html', user=current_user)
    

     
@app.route('/recoveruser/user',methods=['POST','GET'])
@login_required
def recover2():
    if request.method == "POST":
        v = request.form.get('password1')
        xx = request.form.get('password2')
        if v == xx:
            password3 = users(password=v)
            db.session.add(password3)
            db.session.commit()
    return render_template('recoveruser.html',user=current_user)


@app.route('/user', methods=["POST","GET"])
@login_required
def user():
        x = requests.get('https://translate.googleapis.com')
        print(x.status_code)
       
        
        

       
        
        
        username = current_user.username
        pfp = current_user.pfp
        if request.method == "POST":
            x1 = request.form.get('data1')
            
            x = date.today()
            x2 = current_user.username
            if x1:
                data2 = data(post=x1,time=x,user_id=x2)
                db.session.add(data2)
                db.session.commit()
                flash('Post added successfully',category='success')
                print(x1)
                return render_template('user.html',user=current_user,x1=x1,pfp=pfp,username=username)
            else:
                flash('Post could\'nt be added', category='error')
                

       

        
            
        return render_template('user.html',user=current_user,pfp=pfp,username=username,x=x)
            
            
           
       
        
        
        

@app.route("/user/<user>", methods=["POST", "GET"])
@login_required
def profile(user):
    email = current_user.email
    username = current_user.username
    pfp = current_user.pfp
    x = request.form.get("pfp")
   
        
    if request.method == "POST":
        if os.path.exists("/" + x):
            x = current_user.pfp
            print(x)
        
            return render_template("profile.html", pfp=pfp,user=current_user,username=username,email=email)

       
       
    return render_template("profile.html", username=username, email=email,user=current_user)
   

    
  



@app.route('/delete-post', methods=["POST","GET","DELETE"])
@login_required
def deletepost():
        pfp = current_user.pfp
        #data1 = current_user.data1
        #db.session.delete(data1)
        #db.session.commit()
    
        return render_template('deletepost.html', user=current_user,pfp=pfp)


    
            


@app.route("/logout")
@login_required
def logout():
        logout_user()
        return redirect(url_for("login"))

@app.route('/delete')
@login_required
def delete():
    usr = current_user
    db.session.delete(usr)
    db.session.commit()
    return redirect(url_for('login'))

    

    





#RUN

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



