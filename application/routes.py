from application import app
from flask import render_template , request , flash , redirect , url_for , session
#from application.form_login import LoginForm

# This section set up the route for login page
@app.route('/')
@app.route('/login')
def loginPage():
    #form = LoginForm()
    return render_template('login.html', title = "Login")