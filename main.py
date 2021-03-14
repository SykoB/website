from flask import Flask, redirect, render_template, session, request, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin



#VARIABLES-->

#FLASK
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3" 
app.config["SQUALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'b\xdb\x87-\x00\x95\x19\r\xe5\xdf*\x99\xb0K\\\xb6\xf8\xb6PN\xf9\x90\xc0p\x90'
app.permanent_session_lifetime = timedelta(minutes=5)
#SQLALCHEMY
db = SQLAlchemy(app)
#LOGIN MANAGER
login_manager = LoginManager()
login_manager.login_view = "login.html"
login_manager.init_app(app)



#DATABASE

class users(db.Model,UserMixin):
    _id = db.Column("id", db.Integer, primary_key="True")
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(id):
    return  users.query.get(int(id))


 
#ROUTES

@app.route('/')
def main():
    return render_template("main.html")




@app.route('/user')
@login_required
def user():
        login_user()
        return render_template("user.html")
        

        


@app.route('/login', methods=["POST","GET"])
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
                  return redirect(url_for("user.html"))
              else:
                  flash("Password incorrect", category="error")
          else:
                  flash("User does not exist", category="error")
          
         
          
        return redirect(url_for("login", user=current_user))
        
   
        
        
    

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
       

        user = users.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", category="error")

        elif len(email) < 7:
            flash("Email must be longer than 6 characters", category="error")
        elif len(username) < 4:
            flash("Username must be longer than 3 characters", category="error")
        elif len(password) < 4:
            flash("Password must be longer than 3 characters", category="error")
        else:
            flash("Account created!", category="success")
            usr = users(email=email,username=username,password=generate_password_hash(password, method="sha256"))
            db.session.add(usr)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("user"))
    return render_template("signup.html", user=current_user)
   
            
    
           

    
            


@app.route("/logout")
@login_required
def logout():
        logout_user()
        return redirect(url_for("main"))
    

    





#RUN

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



