from application import app
from flask import render_template , request , flash , redirect , url_for , session
# This line import the login form
from application.form_login import LoginForm
# This line import the login table
from application.login_model import Login_Entry
# This line import sqlite database
from application import db
from flask import jsonify

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
        return redirect(url_for("mainPage"))

@app.route('/main')
def mainPage():
    if "user" in session:
        user = session["user"]
        print(user)
        return render_template('Feedback.html',title ="Main")
    else:
        flash("Please login first!","danger")
        return redirect(url_for("loginPage"))

@app.route('/login_complete',methods = ['GET','POST'])
def login_user():
    if "user" in session:
        return redirect(url_for("mainPage"))
    else:
        form = LoginForm()
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.name.data
                password = form.password.data
                name_check = Login_Entry.query.filter_by(username = name).first()
                # Checks if the user exists
                if name_check is None:
                    flash("User does not exist!","danger")
                    return render_template("Login.html",form = form)
                else:
                    name_password = name_check.password
                    #If the user exists, check if the password is correct
                    if name_password != password:
                        flash("Wrong Password!","danger")
                        return render_template("Login.html",form = form)
                    # If the login is successful, include the user id in the parameter
                    else:
                        
                        user_id = name_check.id
                        session['user'] = user_id
                        return redirect(url_for('mainPage'))
        else:
            flash("Please login first!","danger")
            return redirect(url_for("loginPage"))


#=================================================================================
#==============================API for testing====================================
#=================================================================================

# Test if the user can register with API
@app.route("/api/register_complete",methods=['POST'])
def api_register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    new_user = Login_Entry(
        username = username,
        password = password
    )
    result = add_login_entry(new_user)
    #print(result)
    return jsonify({
        'id' : result
    })

def add_login_entry(login_entry):
    try:
        db.session.add(login_entry)
        db.session.commit()
        return login_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")