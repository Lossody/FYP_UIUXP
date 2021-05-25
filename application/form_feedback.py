from flask_wtf import FlaskForm
from wtforms import SubmitField , StringField, RadioField , SelectField
from wtforms.validators import Length, InputRequired , ValidationError , NumberRange , Regexp

class FeedbackForm(FlaskForm):
    stars = RadioField('Stars',choices=[('5','5'),('4','4'),('3','3'),('2','2'),('1','1')],validators = [InputRequired()])
    category = SelectField('Password',choices=[('A','A'),('B','B'),('C','C')],validators = [InputRequired()])
    feedback = StringField('feedback',validators = [Length(1,300)])
    submit = SubmitField("Submit")