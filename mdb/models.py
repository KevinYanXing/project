# -*- coding: utf-8 -*-
'''
Created on 2011-4-23

@author: kevin
'''
from flask import abort
from werkzeug import cached_property
# from flask.ext.principal import RoleNeed, UserNeed,Permission
import re
from time import time
from .pagination import Paged
from bson import ObjectId

class Models(object):
    '''
    将字典的数据转换成直接属性访问
    '''
    # 必须设置这个东西
    db = None

    def __init__(self,data = None):
        if not data:data = {}
        self.data = data
        self.old_data = data.copy()
        self.update = {}

    def __getattr__(self, attr):
        if attr == 'mongo_id':
            attr = '_id'
        ret = self.data.get(attr,'')
        return ret

    def __setattr__(self, key, value):
        if key in ['data', 'old_data', 'update']:
            return super.__setattr__(self, key, value)
        if key == 'mongo_id':
            key = '_id'
        self.data[key] = value

        if key != '_id':
            self.update[key] = value

    @classmethod
    def getDb(cls):
        raise Exception,u'子类必须重载此方法'

    # @cached_property
    # def permissions(self):
    #     '''
    #     权限检查，调用Permissions类,
    #     '''
    #     return Permissions(self)

    def valid_str(self, val, length=[1, 100], only=True):
        """
        验证字符输入
        :param val:待验证的字符
        :param length:长度范围
        """
        if length[0] > 0 and val is None: return -1
        if val:
            #val = val.trim()
            if len(val) >= length[1] or len(val) <= length[0]: return -2
            if only: return self.valid_clean_str(val)
        return True

    def valid_clean_str(self, val):
        """
        不允许任何的标点符号,只允许中文，英文，数字
        """
        q = re.compile(ur'[A-Za-z0-9\u4e00-\u9fa5]+$', re.IGNORECASE)
        if q.match(val): return True
        else: return False

    def valid_num(self, val):
        """
        验证是否数字
        """
        if not val: return -1
        try:
            val = float(val)
        except: return False
        return True

    @classmethod
    def get_or_404(cls, id, d_tb_name=None):
        ret = cls.one(id, d_tb_name=d_tb_name)
        if not ret:
            return abort(404)
        return ret

    @classmethod
    def one(cls, id, d_tb_name=None):
        ret = cls.rundb(method='item', id=id, d_tb_name=d_tb_name)
        if ret:
            ret['d_tb_name'] = d_tb_name
            return cls(ret)
        return None

    @classmethod
    def all(cls, d_tb_name=None):
        """
        获取所有
        """
        ret = []
        datas = cls.rundb(method='find', query={}, d_tb_name=d_tb_name)
        for item in datas:
            item['d_tb_name'] = d_tb_name
            ret.append(cls(item))
        return ret

    @classmethod
    def search(cls, page=1, nums=30, sort=None, json=False, d_tb_name=None, **kw):
        """
        根据制定的数据查询并返回带页数
        如果要查询某个范围内的值，请直接指定类似： d = [1,100]
        其他复杂的检索这里做不到，要自行实现
        """

        where = cls._build_where(**kw)
        #where,sort,page,per_page
        datas = cls.rundb(method='query', where=where, sort=sort, page=page, per_page=nums, d_tb_name=d_tb_name)
        ret = []
        if datas:
            if not json:
                for item in datas['d']:
                    item['d_tb_name'] = d_tb_name
                    ret.append(cls(item))
            else:
                from bson import ObjectId
                for item in datas['d']:
                    for k, v in item.iteritems():
                        if type(v) == ObjectId:
                            item[k] = str(v)
                        item['d_tb_name'] = d_tb_name
                    ret.append(item)
        else:
            return Paged(datas=ret, page=page, per_page=nums, total=0)

        return Paged(datas=ret, page=page, per_page=nums, total=datas['l'])

    @classmethod
    def _build_where(cls, **kw):
        """
        生成条件
        """
        where = {}
        for item in kw.keys():
            val = kw[item]
            if item[0]!='$' and type(val) in [set,list] and len(val) == 2:
                where[item] = {'$lte':val[1],'$gte':val[0]}
            else:
                where[item] = val
        return where

    @classmethod
    def drop(cls, d_tb_name=None):
        return cls.rundb(method='drop', d_tb_name=d_tb_name)

    @classmethod
    def ensure_index(cls, d_tb_name=None, background=True, **kw):
        """
        创建索引
        """
        indexs = []
        for k,v in kw.iteritems():
            indexs.append((k, v))
        return cls.rundb(method='ensure_index', item =indexs, d_tb_name=d_tb_name, background=background)

    @classmethod
    def rename(cls, new_name, d_tb_name=None):
        """
        重新命名集合
        :param new_name:
        :param kw:
        :return:
        """
        return cls.rundb(method='rename', new_name=new_name, d_tb_name=d_tb_name)

    @classmethod
    def findone(cls, d_tb_name=None, select=None, **kw):
        """
        根据条件获取单条
        """
        where = cls._build_where(**kw)

        ret = cls.rundb(method='findone', query=where, select=select, d_tb_name=d_tb_name)
        if ret:
            ret['d_tb_name'] = d_tb_name
            return cls(ret)
        return None

    @classmethod
    def query(cls, sort=None, d_tb_name=None, select=None, **kw):
        """
        根据条件查找全部内容
        """
        where = cls._build_where(**kw)
        #def find(self,query,sort = None):
        datas = cls.rundb(method='find', query=where, sort=sort, select=select, d_tb_name=d_tb_name)
        ret = []
        for item in datas:
            item['d_tb_name'] = d_tb_name
            ret.append(cls(item))
        return ret

    @classmethod
    def top(cls, sort, nums, skip=0, d_tb_name=None, **kw):
        """
        获取最前面多少条
        """
        where = cls._build_where(**kw)
        if skip:
            datas = cls.rundb(method="top", skip=skip, sort=sort, nums=nums, where=where, d_tb_name=d_tb_name)
        else:
            datas = cls.rundb(method="top", sort=sort, nums=nums, where=where, d_tb_name=d_tb_name)
        ret = []
        for item in datas:
            item['d_tb_name'] = d_tb_name
            ret.append(cls(item))
        return ret

    @classmethod
    def aggregate(cls, match, group, sort=None, top=None, skip=None, unwind=None, project=None, d_tb_name=None):
        """
        聚合
        :param match:
        :param group:
        :param sort:
        :param top:
        :return:
        """
        where = [{'$match': match}, {'$group': group}]
        if project:
            where.append({'$project': project})
        if sort:
            where.append({'$sort': sort})

        return cls.rundb(method='aggregate', where=where, top=top, skip=skip, unwind=unwind, d_tb_name=d_tb_name)

    @classmethod
    def aggregate_s(cls, where, d_tb_name=None):
        """
        聚合的原始方法
        :param where:
        :param d_tb_name:
        :return:
        """
        return cls.rundb(method='aggregate_s', where=where, d_tb_name=d_tb_name)

    @classmethod
    def find_s(cls, sort=None, d_tb_name=None, select=None, **kw):
        """
        find的原始方法
        :param sort:
        :param d_tb_name:
        :param select:
        :param **kw:
        :return:
        """
        where = cls._build_where(**kw)
        return cls.rundb(method='find', query=where, sort=sort, select=select, d_tb_name=d_tb_name)

    @classmethod
    def minsert(cls, items, d_tb_name=None):
        """
        批量写入
        :param items:
        :return:
        """
        return cls.rundb(method='minsert', items=items, d_tb_name=d_tb_name)

    @classmethod
    def mremove(cls, where, d_tb_name=None):
        """
        根据条件批量清除
        :param where:
        :param d_tb_name:
        :return:
        """
        return cls.rundb(method='mremove', where=where, d_tb_name=d_tb_name)

    def remove(self, d_tb_name=None):
        """
        删除
        """
        #return db.S_xml_delete(id = self.mongo_id)
        self.beforeRemove()
        ret = self.rundb(method='delete', id=self.mongo_id, d_tb_name=d_tb_name)
        self.afterRemove()

        return ret

    def afterRemove(self):
        pass

    def addsave(self, d_tb_name=None):
        """
        将数据更新或者保存
        """
        self.beforeAdd()
        return self.rundb(method='save', d_tb_name=d_tb_name, **self.data)

    def save(self, d_tb_name=None):
        """
        编辑或者新增
        """
        if self.mongo_id:
            if self.update and self.update!={}:
                self.beforeUpdate()
                self.rundb(method='update', id=self.mongo_id, d_tb_name=d_tb_name, **self.update)
                self.afterUpdate()
            return self.mongo_id
        else:
            self.beforeAdd()
            if 'd' not in self.data.keys():
                self.data['d'] = time()
            id = self.rundb(method='add', d_tb_name=d_tb_name, **self.data)
            self._id = id
            self.afterAdd()
            return id

    def add(self, d_tb_name=None):
        """
        直接执行增加操作
        """
        self.beforeAdd()
        id = self.rundb(method='add', d_tb_name=d_tb_name, **self.data)
        self._id = id
        self.afterAdd()
        return self._id

    def beforeRemove(self):
        """
        在删除之前要做的事情
        """
        pass

    def beforeUpdate(self):
        """
        在编辑之前可以操作的
        """
        pass

    def beforeAdd(self):
        """
        在添加之前可以做的
        """
        pass

    def afterUpdate(self):
        """
        在编辑之前可以操作的
        """
        pass

    def afterAdd(self):
        """
        在添加之前可以做的
        """
        pass

    @classmethod
    def getService(cls, d_tb_name=None):
        """
        获取类名，也可以重载
        """
        if d_tb_name:
            return d_tb_name

        if hasattr(cls,'Tablename'):
            return cls.Tablename
        return cls.__name__.lower()

    @classmethod
    def upcmd(cls, where, update, upsert=True, multi=True, d_tb_name=None):
        """
        执行更新命令
        """
        return cls.rundb("upcmd", where=where, update=update, upsert=upsert, multi=multi, d_tb_name=d_tb_name)

    @classmethod
    def distinct(cls, key_name, d_tb_name=None, **kw):
        """
        返回去重指定键名的统计结果
        """
        where = cls._build_where(**kw)
        return cls.rundb('distinct', key_name=key_name, where=where, d_tb_name=d_tb_name)

    @classmethod
    def rundb(cls, method, d_tb_name=None, **kw):
        """
        执行
        """
        if not cls.db:
            raise Exception,u'请设置类的 db = db'

        return cls.db.rpc_method(method=method, ex_service=cls.getService(d_tb_name), **kw)

    @classmethod
    def count(cls, d_tb_name=None, **kw):
        """
        根据条件计算条数
        """
        where = cls._build_where(**kw)
        return cls.rundb("count", query=where, d_tb_name=d_tb_name)

    @classmethod
    def getIndexes(cls, d_tb_name=None):
        """
        获取索引列表
        """
        return cls.rundb("getIndexes", d_tb_name=d_tb_name)

    @cached_property
    def date_str(self):
        from datetime import datetime
        if self.d:
            return datetime.fromtimestamp(self.d).strftime('%Y-%m-%d %H:%M:%S')
        return u'不存在'


class ChildModel(object):
    """
    获取子文档的数据，并更新或者新增
    """

    _parent = Models

    def __init__(self, pid, data=None):
        if not data:
            data = {}
        self._data = data
        self._update = {}
        self._pid = pid

        # for k, v in self._data.iteritems():
        #     setattr(self, k, v)

    def __getattr__(self, attr):
        if attr in ['_parent']:
            return super.__getattribute__(self, attr)

        if attr == 'mongo_id':
            attr = '_id'
        ret = self._data.get(attr, '')
        return ret

    def __setattr__(self, key, value):
        if key in ['_data', '_update', '_pid', '_parent']:
            return super.__setattr__(self, key, value)

        if key == 'mongo_id':
            key = '_id'

        self._data[key] = value

        if key != '_id':
            self._update[key] = value

    def save(self, force=False):
        """
        保存到数据库中
        :param force: 是否强制新增
        :return:
        """
        if not force and self._data.get('_id'):
            return self._edit()
        else:
            return self._add()


    def _add(self):
        """
        新增到数据库中
        :return:
        """
        update = self._update.copy()
        if self.mongo_id:
            update['_id'] = self.mongo_id
        else:
            update['_id'] = ObjectId()

        self._parent.upcmd(where={'_id': self._pid},
                          update={'$push': {self.selfname(): update}},
                          upsert=False, multi=False)
        self._data['_id'] = update['_id']
        return self.mongo_id


    def _edit(self):
        """
        更新到数据库中
        :return:
        """
        update = dict()
        cls_name = self.selfname()
        for k, v in self._update.iteritems():
            update['%s.$.%s' % (cls_name, k)] = v
        self._parent.upcmd(where={'_id': self._pid, '%s._id' % cls_name: self.mongo_id}, upsert=False, multi=False,
                          update={'$set': update})
        return self.mongo_id

    def remove(self):
        """
        删除文档
        :return:
        """
        self._parent.upcmd(where={'_id': self._pid, '%s._id' % self.selfname(): self.mongo_id},
                           update={
                               '$pull': {self.selfname(): {'_id': self.mongo_id}}
                           }
        )


    @classmethod
    def selfname(cls):
        return cls.__name__.lower()

    @classmethod
    def one(cls, parent_id, child_id):
        """
        获取指定ID 的子文档
        :param cid:  子文档ID
        :param pid:  父文档ID
        :return:
        """
        # {"albums":{$elemMatch:{privilege:5}}}

        where = {'_id': parent_id, '%s._id' % cls.selfname(): child_id}
        select = {cls.selfname(): {'$elemMatch': {'_id': child_id}}}
        data = cls._parent.findone(select=select, **where)
        data = data.data.get(cls.selfname())
        if data:
            return cls(parent_id, data[0])
        else:
            return None

    @classmethod
    def findOne(cls, where, kwargs, others=[]):
        """
        获取指定条件的子文档
        :param where: 条件
        :param kwargs:  子文档条件
        :return:
        """
        # where = {'_id': pid, '%s._id' % cls.selfname(): cid}
        for k, v in kwargs.iteritems():
            where['{0}.{1}'.format(cls.selfname(), k)] = v

        select = {cls.selfname(): {'$elemMatch': kwargs}}
        for item in others:
            select[item] = 1
        data = cls._parent.findone(select=select, **where)
        if data:
            pid = data.mongo_id
            ret = data.data.get(cls.selfname())
            ret = ret[0]
            for item in others:
                ret['p_{0}'.format(item)] = data.data.get(item)
            return cls(pid, ret)
        else:
            return None

    @classmethod
    def find(cls, where, others=None, **child_select):
        """
        获取所有子文档列表
        :param where: 查询条件,必须是要字典()
        :param others: 额外返回的数据(数组,比如:[sid, d]), 这些数据将在child的p_字段名的形式存放
        :param child_select: 子文档的筛选
        :return:
        """
        key = cls.selfname()
        c_select = {}
        for k, v in child_select.iteritems():
            where['%s.%s' % (key, k)] = v
            c_select[k] = v
        select = {}
        if c_select:
            select[key] = {'$elemMatch': select}
        if others:
            for oth in others:
                select[oth] = 1
        if not select:
            select = None
        # print where, select
        data = cls._parent.query(select=select, **where)
        ret = []
        for item in data:
            tmp = item[key]
            for oth in others:
                tmp['p_{0}'.format(oth)] = item[oth]
            ret.append(cls(item['_id'], tmp))
        return ret

    @cached_property
    def parent(self):
        """
        返回父类
        :return:
        """
        return self._parent.one(self._pid)

    @classmethod
    def query(cls, match, child_match, others=None):
        """
        数据查询
        :param match: 主文档条件
        :param child_match: 子文档条件
        :param others: 额外返回的数据(数组,比如:[sid, d]), 这些数据将在child的p_字段名的形式存放   ---  暂时没有实现
        :return:
        """
        prop_name = cls.selfname()
        query = [
            {'$match':match},
            {'$unwind':'${0}'.format(prop_name)}
        ]
        if child_match:
            query.append({'$match':child_match})
        ret = cls._parent.aggregate_s(query)
        if ret.get('ok') == 1:
            ret = ret['result']
            datas = []
            for item in ret:
                tmp = item[prop_name]
                tmp['_{0}_id'.format(prop_name)] = item['_id']
                datas.append(cls(item['_id'], tmp))
            if len(datas) == 1:
                return datas[0]
            return datas

    @classmethod
    def pager(cls, match, sort, others, pagesize=30, page=1):
        """
        数据检索,并分页
        :param match: 检索条件, {_id:{$in:['3437efc919a0501570186bf7c26daf7c']}}
        :param sort: 排序方式 {'p.tr':-1}
        :param others: 需要额外加入的键,比如 ['sid', 'd'], 在文档里面将是p_ 的形式存在
        :param pagesize: 单页大小
        :param page: 当前页
        :return:
        """

        prop_name = cls.selfname()
        group = {
            '_id': '$_id',
            prop_name: {'$addToSet': '$' + prop_name}
        }
        project = {
            '_id': 1,
            'size': {'$size': '$' + prop_name},
            prop_name: {
                '$slice': ['$' + prop_name,(page - 1) * pagesize,page * pagesize]
            }
        }
        for oth in others:
            group[oth] = {'$first':'${0}'.format(oth)}
            project[oth] = 1
        query = [
            {'$match':match},
            {'$unwind':'$' + prop_name},
            {'$sort':sort},
            {'$group':group},
            {'$project':project}
        ]
        ret = cls._parent.aggregate_s(query)
        if ret.get('ok') == 1:
            ret = ret['result'][0]
            total = ret['size']
            data = []
            for item in ret['p']:
                tmp = item
                for oth in others:
                    tmp['p_{0}'.format(oth)] = ret[oth]
                data.append(cls(item['_id'], tmp))

            return Paged(data, page, pagesize, total)
#
# class Permissions(object):
#     '''
#     权限类
#     '''
#     def __init__(self, obj):
#         '''
#         实例化权限，参数obj为本对象数据
#         '''
#         self.obj = obj
#
#     @cached_property
#     def delete(self):
#         '''
#         删除权限检查，返回True或False
#         '''
#         return Permission(RoleNeed('admin')) or Permission(UserNeed(self.obj.u))
#
#     @cached_property
#     def allow_edit(self):
#         '''
#         返回True或False
#         '''
#         return Permission(RoleNeed('admin')) or Permission(UserNeed(self.obj.u))
#
#     @cached_property
#     def view(self):
#         '''
#         访问权限检查，返回True或False
#         '''
#         return Permission(RoleNeed('admin')) or Permission(UserNeed(self.obj.u))