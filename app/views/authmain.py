from flask import Blueprint,send_from_directory,abort,redirect,url_for,render_template
import os
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

@authmain.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('frontend.index'))

@authmain.route('/personal/info')
@login_required
def personal_info():
    return render_template('authmain/personal_info.html')