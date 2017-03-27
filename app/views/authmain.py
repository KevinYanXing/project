from flask import Blueprint,send_from_directory,abort,redirect,url_for
import os
from flask_login import logout_user

authmain = Blueprint('authmain', __name__)

@authmain.route('/upload/<string:pho>/', methods=['GET', 'POST'])
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
def logout():
    logout_user()
    return redirect(url_for('frontend.index'))