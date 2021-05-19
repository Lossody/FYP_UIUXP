# This line import the database
from application import db

class Login_Entry(db.Model):
    __tablename__ = "User_Table"

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    position = db.Column(db.String)
