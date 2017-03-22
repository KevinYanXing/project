from flask_wtf import FlaskForm,file
from wtforms import StringField, SubmitField,DateField,PasswordField,DateTimeField,TextAreaField,FileField
from fsuper import SDateField
from wtforms.validators import Required,required
from flask import redirect,url_for


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    birthday = SDateField('when is your birthday?', validators=[Required()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    n = StringField(label='Your name:', validators=[Required()],description='Please input your name:')

    submit = SubmitField('Submit')



