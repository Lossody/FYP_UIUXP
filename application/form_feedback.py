from flask_wtf import FlaskForm
from wtforms import SubmitField , StringField, RadioField , SelectField
from wtforms.validators import Length, InputRequired , ValidationError , NumberRange , Regexp

class FeedbackForm(FlaskForm):
    stars = RadioField('Stars',choices=[('1','Very Unsatisifed'),('2','UnSatisfied'),('3','Somewhat Satisifed'),('4','Satisfied'),('5','Very Satisfied')],validators = [InputRequired()])
    category = SelectField('Password',choices=[('Leave/Time off','Leave and time off benefits'),('Break Periods','Meal and break periods'),('Timekeeping/Pay','Timekeeping and pay')],validators = [InputRequired()])
    feedback = StringField('feedback',validators = [Length(1,300)])
    submit = SubmitField("Submit")