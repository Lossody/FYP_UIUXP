# This line import the database
from application import db

class Feedback_Entry(db.Model):
    __tablename__ = "Feedback_Table"

    feedback_id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String)
    category = db.Column(db.String)
    feedback = db.Column(db.String)
    position = db.Column(db.String)
