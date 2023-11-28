from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import  DataRequired

class TodoForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()]) #this mező must be filled
    description = TextAreaField("Description", validators=[DataRequired()])
    completed = SelectField("completed", choices=[("False", "False"), ("True", "True")])
    validators = [DataRequired()]
    submit_button = SubmitField("Add todo")

