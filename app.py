
#import flask framework
from flask import Flask,render_template,request,session,redirect,flash,url_for
import pandas as pd
from passlib.context import CryptContext
from datetime import datetime
import os
from forms import LoginForm,RegisterForm
from models import db,LoginUser,pwd_context
from functools import wraps


#initialization flask app
app = Flask(__name__)

app.secret_key = os.urandom(56)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Manu_sid123@localhost/db_school?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def login():
    form = LoginForm()
    return render_template("login.html",form=form)


@app.route('/register')
def register():
    form = RegisterForm()
    return render_template("register.html",form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    form = LoginForm()
    if request.method == "POST":

        email = form.email.data
        password = form.password.data

        user = LoginUser.query.filter_by(email=email).first()
    
        if user:
            if pwd_context.verify(password, user.pass_word) and password=="111111":
                session.permanent = True
                session['user_id'] = user.email
               
                return render_template("reset.html")
            elif pwd_context.verify(password, user.pass_word) and (user.user_status=="User"):
                session.permanent = True
                session['user_id'] = user.email
                session['user_status'] = user.user_status
                return render_template("home.html")
            
            elif pwd_context.verify(password, user.pass_word) and (user.user_status=="Admin"):
                session.permanent = True
                session['user_id'] = user.email
                session['user_status'] = user.user_status
                users = LoginUser.query.all()
                return render_template("admin_panel.html",payload=users)

            else:
                flash("Kindly provide valid email id and password.")
                return render_template("login.html", form=form)
        else:
            flash("This email id is not registered with us.")
            return render_template("login.html", form=form)
    else:
        flash("Please eneter valid email id and password to proceed.")
        return render_template("login.html", form=form)

@app.route('/add_user',methods=['POST'])
def add_user():
    form = RegisterForm()
    if request.method == "POST":

        email = form.email.data
        print("email",email)
        password = form.password.data
        passw = pwd_context.encrypt(password)
        dt = datetime.now()
        
            #check the existing user

        user = LoginUser.query.filter_by(email=email).first()

        if user:
            flash("This email id is already exist")
            return render_template("register.html",form =form)
        
        else:
            user = LoginUser(
                email=form.email.data,
                pass_word=passw,
                user_status='user',
                dt_time = dt
                            )
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully.Please contact Admin to Login.")
        return render_template("register.html",form=form)
        
   
        
    return render_template("register.html",form=form)


@app.route('/reset', methods=["POST", "GET"])
def reset():
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        email = session['user_id']

        if password != confirm_password:
            flash("Password do not match", 'danger')
            return redirect('/reset')
        
       
        user = LoginUser.query.filter_by(email=email).first()             
        
        passw = pwd_context.encrypt(password)
        user.pass_word = passw
        db.session.commit()
        flash("Password reset successfully.")
        
    return render_template('reset.html')
        
        



@app.route('/approve_user', methods=["GET", "POST"])
def approve_user():
    if 'user_id' in session:
        if request.method == 'POST':
            
            ids_checked = request.form.getlist('check')
            user_status = request.form.get('user_level')
           
            
            
            if ids_checked:
                
               
                
                for id in ids_checked :
                    if user_status!="reset":
                        user = LoginUser.query.filter_by(id=id).first()
                        user.user_status = user_status
                        db.session.commit()
                        flash("Selected user access changed successfully.")
                        users = LoginUser.query.all()
                        return render_template('admin_panel.html', payload=users)
                    else:
                        user = LoginUser.query.filter_by(id=id).first()
                        print("user :\n",user)
                        password = "111111"
                        passw = pwd_context.encrypt(password)
                        user.pass_word = passw
                        db.session.commit()
                        flash("Password reset successfully.")
                        users = LoginUser.query.all()
                        return render_template('admin_panel.html', payload=users)

            else:
                flash(" No User selected for Access Change !!")
        else:
            return redirect('/')

if __name__ == '__main__':

    app.run(debug=True, host="localhost", port=8080)








