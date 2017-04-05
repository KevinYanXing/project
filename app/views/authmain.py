from flask import Blueprint,send_from_directory,abort,redirect,url_for
import os
from app.help import Help
from app.forms.mainform import UsereditForm
from flask_login import logout_user,login_required

authmain = Blueprint('authmain', __name__)

@authmain.route('/upload/<string:pho>/', methods=['GET', 'POST'])
@login_required
def upload(pho):
    if not pho:
        return abort(404)
    from flask import current_app
    apppth = current_app.config.get('UPLOAD_DEST')
    path = os.path.join(apppth, pho)
    pth = os.path.dirname(path)
    filename = os.path.basename(path)
    return send_from_directory(pth, filename, add_etags=False, cache_timeout=2592000)

@authmain.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('frontend.index'))

@authmain.route('/personal/info/')
@login_required
def personal_info():
    return Help.render('authmain/personal_info.html')

@authmain.route('/personal/info/edit/', methods=['GET', 'POST'])
def personal_info_edit():
    form = UsereditForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.index'))
    return Help.render('authmain/personal_info_edit.html', form=form)