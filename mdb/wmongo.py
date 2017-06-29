# coding=utf-8
from basedb import BaseDB
from dredis import DRedis
import connection

from pymongo import MongoClient
#
#
class WMongo(object):
    """
    MONGODB类
    """

    def __init__(self):
        self.app = None
        self.conns = {}

    def init_app(self, app, dbs):
        self.app = app
        self.dbs = dbs
        self.status_redis = None
        if app.config.get('DB_STATUS_REDIS_URL'):
            self.status_redis = DRedis()
            self.status_redis.init_app(app, 'DB_STATUS_REDIS_')

    def conn(self, db):
        # 检查这个db是否存在切换记录
        if self.status_redis:
            status = self.status_redis.get('SWITCH.{0}'.format(db))
            if status:
                # 直接redis里面记录的就是当前要读的数据库编号
                db = '{0}_{1}'.format(db, status)

        if self.conns.get(db):
            return self.conns[db]

        if db:
            prex = db + '_'
        else:
            prex = ''

        conn_settings = self.app.config.get(prex + 'MONGODB_SETTINGS', None)
        if not conn_settings:
            conn_settings = {
                'db': self.app.config.get(prex + 'MONGODB_DB', None),
                'username': self.app.config.get(prex + 'MONGODB_USERNAME', None),
                'password': self.app.config.get(prex + 'MONGODB_PASSWORD', None),
                'host': self.app.config.get(prex + 'MONGODB_HOST', None),
                'port': int(self.app.config.get(prex + 'MONGODB_PORT', 0)) or None,
                'use_greenlets': self.app.config.get(prex + 'USE_GREENLETS', False),
                'alias':db
            }
        try:
            ret = MongoClient(host=conn_settings['host'], port=conn_settings['port'])[conn_settings['db']]
        except Exception, ex:
            ex.message = str(conn_settings)
            raise ex 

        self.conns[db] = ret
        return ret

    def __getitem__(self, item):
        return MDB(item, self)

    def __getattr__(self, item):
        if item not in ['app', 'connection'] and item[0] != '_':
            return MDB(item, self)


class MDB(BaseDB):
    """
    内部类库
    """
    def collection(self, table_name):
        return self.db()[table_name]

    def db(self):
        return self.db_self.conn(self.db_name)