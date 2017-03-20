# coding=utf-8
from flask import render_template, session, redirect, url_for, flash,Blueprint
from app.forms.mainform import NameForm
from mdb.kndb.main import Kn
frontend = Blueprint('frontend', __name__)

@frontend.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_birth = session.get('birth')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_birth is not None and old_birth != form.birthday.data:
            flash('Looks like you have changed your brthday!')
        session['name'] = form.name.data
        session['birth'] = form.birthday.data
        return redirect(url_for('frontend.index'))
    return render_template('frontend/index.html', form=form, name=session.get('name'),birth=session.get('birth'))