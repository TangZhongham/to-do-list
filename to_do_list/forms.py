from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    label = StringField('label', validators=[DataRequired()])
