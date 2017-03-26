from flask_wtf import FlaskForm,file
from wtforms import StringField, SubmitField,DateField,PasswordField,FileField
from fsuper import SDateField
from flask_wtf.file import FileRequired,FileAllowed
from wtforms.validators import Required,required
from flask import redirect,url_for
from flask_login import login_user
from mdb.kndb.main import Kn,User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    birthday = SDateField('when is your birthday?', validators=[Required()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    name = StringField('Your name', validators=[Required()])
    pwd = PasswordField('Your password',validators=[Required()])
    rppwd = PasswordField('Repeat password',validators=[Required()])
    birth = SDateField('Your birthday', validators=[Required()])
    pho = FileField('Your head portrait',validators=[FileRequired(),FileAllowed(['jpg','png'],'Please upload images')])
    submit = SubmitField('Submit')

    def validate_rppwd(self,field):
        if field.data != self.pwd.data:
            raise ValueError, 'Please repeat the password correctly!'

class SigninForm(FlaskForm):
    name = StringField('Your name', validators=[Required()])
    pwd = PasswordField('Your password',validators=[Required()])
    submit = SubmitField('Submit')

    def validate_pwd(self,field):
        user = User.findone(name=self.name.data)
        if user is not None and user.verify_password(self.pwd.data):
            login_user(user)
        else:
            raise ValueError, 'Invalid username or password.'


