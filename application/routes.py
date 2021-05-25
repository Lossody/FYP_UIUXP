from application import app
from flask import render_template , request , flash , redirect , url_for , session
# This line import the login form and the register form
from application.form_login import LoginForm
from application.form_register import RegisterForm
from application.form_update import UpdateForm
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

# This section is for the main page, any people can access it.
@app.route('/main')
def mainPage():
    if "user" in session:
        user = session["user"]
        print(user)
        return render_template('statistics.html',title ="Main")
    else:
        flash("Please login first!","danger")
        return redirect(url_for("loginPage"))

@app.route('/login_complete',methods = ['GET','POST'])
def loginPageComplete():
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

# This is the register section, only the CEO and Secretary and employer can access it
@app.route('/register',methods = ['GET','POST'])
def registerPage():
    if "user" in session:
        user = session['user']
        # This section check if the user is a secretary or CEO
        name_check = Login_Entry.query.filter_by(id = user).first()
        role = name_check.position
        print("Role:",role)
        if role == "C" or role == "S" or role == "ER":
            form = RegisterForm()
            return render_template('register.html',form = form, title = "Registration")
        else:
            flash("Permission denied, seek higher up for assistance.")
            return redirect(url_for("mainPage"))
    else:
        flash("Please login first!","danger")
        return redirect(url_for("loginPage"))

@app.route('/register_complete',methods = ['GET','POST'])
def registerPageComplete():
    form = RegisterForm()
    if request.method == "POST":
        print(form)
        if form.validate_on_submit() == True:
            username = form.name.data
            checker = Login_Entry.query.filter_by(username = username).first()
            # Check if the user exists in the data base
            if checker is None:
                print("YES")
                username = form.name.data
                password = form.password.data
                position = form.position.data
                new_user = Login_Entry( username = username, password = password , position = position)
                add_login_entry(new_user)
                flash("Account Register Succesfully!","success")
                return render_template('register.html',form = form ,title="Registeration")
            else:
                
                flash("Account Already Registered!","danger")
                return render_template('register.html',form = form ,title="Registeration")
        else:
            username = form.name.data
            password = form.password.data
            print(username,password)
            flash("Error creating an Account.","danger")
            return render_template('register.html',form = form)
    else:
        return redirect(url_for("mainPage"))



# This function goes together with the registeration page
# It checks if the user is the CEO or Secretary
def getRole(ids):
    try:
        entries = Login_Entry.query.filter_by(id = int(ids))
        print(entries)
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

# Adds new user in the user table
def addUser(login_entry):
    try:
        db.session.add(login_entry)
        db.session.commit()
        return login_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")


# This section shows the employee table, only CEO and Secretary can see it
@app.route('/viewer')
def viewerPage():
    if "user" in session:
        user = session['user']
        # This section check if the user is a secretary or CEO
        name_check = Login_Entry.query.filter_by(id = user).first()
        role = name_check.position
        print("Role:",role)
        if role == "C" or role == "S":
            return render_template('viewer.html',entries = get_entries())
        else:
            flash("Permission denied, seek higher up for assistance.")
            return redirect(url_for("mainPage")) 
    else:
        flash("Please login first!","danger")
        return redirect(url_for("loginPage"))

# This section removes the employee account, online CEO and secretary can use this function
@app.route('/remove',methods=['GET','POST'])
def remove():
    if "user" in session:
        user = session['user']
        # This section check if the user is a secretary or CEO
        name_check = Login_Entry.query.filter_by(id = user).first()
        role = name_check.position
        if role == "C" or role == "S":
            if request.method == "POST":
                req = request.form
                id = req['id']
                # Check if the entry is empty
                if Login_Entry.query.get(id) != None:
                    # If the entry is not empty, check if it is the CEO
                    remove_role = Login_Entry.query.get(id)
                    if remove_role.position == "C":
                        flash("You cannot remove the CEO!")
                        return render_template("viewer.html",entries = get_entries(),index = True)
                    else:
                        remove_entry(id)
                        return render_template("viewer.html",entries = get_entries(),index = True)
                else:
                    return render_template("viewer.html",entries= get_entries(), index = True)
            else:
                return redirect(url_for('historyPage'))
        else:
            flash("Permission denied, seek higher up for assistance.")
            return redirect(url_for("mainPage"))
    else:
        flash("Please login first!","danger")
        return redirect(url_for("loginPage"))

@app.route('/updater',methods=['GET','POST'])
def updatePage():
    if "user" in session:
        get_id = request.args.get('id_update')
        form = UpdateForm()
        # Check which position is the user for logged in
        user = session['user']
        name_check = Login_Entry.query.filter_by(id = user).first()
        role = name_check.position
        # Checks the role of the person who is going to have their profile updated
        #req = request.form
        #id = req['id']
        result = Login_Entry.query.filter_by(id = get_id).first()
        role_change = result.position
        role_id = result.id
        # If the person is a CEO
        if role == "C":
            return render_template('update.html',entry = role_id,form = form)
        # If the person is a secretary
        elif role == "S":
            if role_change == "C":
                flash("Permission denied, seek higher up for assistance.")
                return redirect(url_for("viewerPage"))
            else:
                return render_template('update.html',entry = role_id,form = form)
        else:
            flash("Permission denied, seek higher up for assistance.")
            return redirect(url_for("mainPage"))
        
    else:
        flash("Please login first!","danger")
        return redirect(url_for("loginPage"))

@app.route('/update',methods=['GET','POST'])
def update():
    if "user" in session:
        form = UpdateForm()
        if request.method == "POST":
            if form.validate_on_submit() == True:
                emp_id = form.emp_id.data
                username = form.name.data
                password = form.password.data
                position = form.position.data
                print("Error check: ",emp_id)
                print(emp_id , username , password , position)
                update_entry(emp_id,username,password,position)
                flash("Update Successful!")
                return redirect(url_for("viewerPage"))
            else:
                return redirect(url_for("viewerPage"))

        else:
            return redirect(url_for("viewerPage"))
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
    position = data['position']
    new_user = Login_Entry(
        username = username,
        password = password,
        position = position
    )
    result = add_login_entry(new_user)
    #print(result)
    return jsonify({
        'id' : result
    })

# This function add user into database
def add_login_entry(login_entry):
    try:
        db.session.add(login_entry)
        db.session.commit()
        return login_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

# This function shows data from the database
def get_entries():
    try:
        entries = Login_Entry.query.all()
        #print(entries)
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

# This function removes user from database
def remove_entry(id):
    try:
        entry = Login_Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")


# This function update user
def update_entry(id,username,password,position):
    try:
        entry = Login_Entry.query.get(id)
        entry.username = username
        entry.password = password
        entry.position = position
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")