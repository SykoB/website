from flask import Flask, redirect, render_template, session, request, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, form
from datetime import timedelta

#VARIABLES

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3" 
app.config["SQUALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'b\xdb\x87-\x00\x95\x19\r\xe5\xdf*\x99\xb0K\\\xb6\xf8\xb6PN\xf9\x90\xc0p\x90'
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

#DATABASE

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key="True")
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

 
#ROUTES

@app.route('/')
def main():
    return render_template("main.html")




@app.route('/user')
def user():
        return render_template("user.html")


@app.route('/login', methods=["POST","GET"])
def login():
        if request.method == "POST":
          
          username = request.form.get("username")
          password = request.form.get("password")
          print(request.form)
          
         
          
          return render_template("user.html")
        else:
            return render_template("login.html")

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
        email = request.form.get("email")
        print(request.form)
       

      
        if len(email) < 7:
            flash("Email must be longer than 6 characters", category="error")
        elif len(username) < 4:
            flash("Username must be longer than 3 characters", category="error")
        elif len(password) < 4:
            flash("Password must be longer than 3 characters", category="error")
        else:
            flash("Account created!", category="success")
    return render_template("signup.html")
    found_user = users.query.filter_by(email=email).first()
    if found_user:
            session["email"] = found_user.email
            flash("User already exists!", category="error")
            
    else:
            usr = users(user,"")
            db.session.add(usr)
            db.session.commit

    
            


@app.route("/logout")
def logout():
        return redirect(url_for("main"))
    

    


@app.route('/database')
def database():
    return render_template("database.html", data=users.query.all())


#RUN

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



