# coding=utf-8
from mdb.ext import db
from mdb.models import Models
from datetime import datetime

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
    用户名:n
    角色:r
    个性签名:s
    头像:p
    其他...
    """
    db = db.USER
