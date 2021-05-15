from application import app
from flask import render_template , request , flash , redirect , url_for , session
# This line import the login form
from application.form_login import LoginForm
# This line import sqlite database
from application import db

# This line creates the database
db.create_all()

# This section set up the route for login page
@app.route('/')
@app.route('/login')
def loginPage():
    if "user" not in session:
        form = LoginForm()
        return render_template('login.html', title = "Login" , form = form)
    else:
        user = session['user']
        return redirect(url_for("mainPage"))

@app.route('/main', methods = ['GET','POST'])
def mainPage():
    if "user" in session:
        return "<h1>Login Successful</h1>"
    else:
        flash("Please Login First!","danger")
        return redirect(url_for("loginPage"))