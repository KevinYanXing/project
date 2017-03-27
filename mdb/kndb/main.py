# coding=utf-8
from mdb.ext import db
from mdb.models import Models
from datetime import datetime
from werkzeug.security import check_password_hash
from bson import ObjectId
from flask_login import UserMixin

def format_ts(ts, format='%Y-%m-%d %H:%M:%S'):
        if not ts:
            return None
        if type(ts) == int:
            ts = float(ts)

        if type(ts) == float:
            ts = datetime.fromtimestamp(ts)
        elif not ts:
            return ''
        format = format.encode('utf-8')
        ret = ts.strftime(format)

        return ret.decode('utf-8')

class Kn(Models):
    """
    时间轴数据库:
    时间:t
    用户id:uid
    图片:p
    内容:c
    标题:b
    其他...
    """
    db = db.KN

class User(Models):
    """
    用户数据库:
    用户名:name
    角色:role
    个性签名:s
    头像:pho
    密码:pwd
    生日:birth
    其他...
    """
    db = db.USER

    from app import login_manager

    @login_manager.user_loader
    def load_user(user_id):
        return User.one(ObjectId(user_id))

    def verify_password(self, password):
        return check_password_hash(self.pwd, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.mongo_id)

    def __repr__(self):
        return '<User %r>' % (self.name)


