# coding=utf-8
from flask import render_template, session, redirect, url_for, flash,Blueprint,g
from app.forms.mainform import NameForm,SignupForm,SigninForm
from mdb.kndb.main import Kn,User
from bson import ObjectId
from time import mktime,strptime,localtime,strftime
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user,current_user
import os

frontend = Blueprint('frontend', __name__)

from flask_login import login_required
@frontend.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@frontend.route('/', methods=['GET', 'POST'])
def index():
    name = ''
    birth = ''
    if current_user.is_authenticated:
        name = current_user.name
        birth = strftime('%Y-%m-%d',localtime(current_user.birth))
    elif session.get('birth'):
        name = session.get('name')
        birth = strftime('%Y-%m-%d',localtime(session.get('birth')))

    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['birth'] = form.birthday.data
        return redirect(url_for('frontend.index'))

    return render_template('frontend/index.html', form=form, name=name,birth=birth)

@frontend.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        birth = form.birth.data
        pho = form.pho.data
        pwd = form.pwd.data
        user = User()
        user.name = name
        user.birth = birth
        pid = ObjectId()
        filename = secure_filename(pho.filename)
        fileformat = os.path.splitext(filename)[1]
        if not os.path.isdir(r'./upload/'):
            os.makedirs(r'./upload/')
        pho.save(r'./upload/'+filename)
        os.rename(r'./upload/'+filename,r'./upload/'+str(pid)+fileformat)
        user.pho = str(pid)+fileformat
        user.pwd = generate_password_hash(pwd)
        flash('Rigister successfully!')
        user.save()
        login_user(user)
        return redirect(url_for('frontend.index'))
    return render_template('frontend/signup.html', form=form)

@frontend.route('/signin/', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.index'))
    return render_template('frontend/signin.html', form=form)
