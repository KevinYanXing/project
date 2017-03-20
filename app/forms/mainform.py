from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    birthday = DateField('when is your birthday?', validators=[Required()])
    submit = SubmitField('Submit')
