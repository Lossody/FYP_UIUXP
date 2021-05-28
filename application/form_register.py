from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField , StringField , PasswordField
from wtforms.fields.core import SelectField
from wtforms.validators import Length, InputRequired , ValidationError , NumberRange , Regexp

class RegisterForm(FlaskForm):
    name = StringField('Username',validators = [InputRequired(),Length(5,20),Regexp(r'^[\w.@+-]+$')])
    password = PasswordField('Password',validators = [InputRequired(),Length(5,20),Regexp(r'^[\w.@+-]+$')])
    position = SelectField('Position',choices=[('S','Secretary'),('ER','Employer'),('E','Employee')],validators = [InputRequired()])
    register = SubmitField("Register")