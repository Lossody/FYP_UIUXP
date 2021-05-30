from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField , StringField , PasswordField
from wtforms.validators import Length, InputRequired , ValidationError , NumberRange , Regexp

class QueryForm(FlaskForm):
    query = StringField("Questions",validators=[InputRequired()])
    search = SubmitField("Search")