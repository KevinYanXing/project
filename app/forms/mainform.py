from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField,PasswordField
from fsuper import SDateField
from wtforms.validators import Required
from flask import redirect,url_for


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    birthday = SDateField('when is your birthday?', validators=[Required()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    n = StringField('Input your your name:', validators=[Required()])
    # b = SDateField('Input your your birthday:', validators=[Required()])
    # m= SDateField('Input your your mobile phone:', validators=[Required()])
    # p = PasswordField('Input your password:', validators=[Required()])
    # rp = PasswordField('Repeat your password:', validators=[Required()])

    submit = SubmitField('Submit')

    def validate_n(self, field):
        print field.data
        raise ValueError,'You may input a fake date =.=!'

    def validate_on_submit(self):
        print 1111111
        return redirect(url_for('frontend.index'))



