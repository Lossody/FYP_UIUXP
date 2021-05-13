from application import app
from flask import render_template , request , flash , redirect , url_for , session


# This section set up the route for login page
@app.route('/login')
def loginPage():
    return "Hello"