# This line import the database
from application import db

class Feedback_Entry(db.Model):
    __tablename__ = "Feedback_Table"

    username = db.Column(db.String)
    feedback = db.Column(db.String)
    position = db.Column(db.String)
