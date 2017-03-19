# coding=utf-8

class BaseDB(object):
    """

    """
    def __init__(self, db_name=None, db_self=None):
        self.db_name = db_name
        self.db_self = db_self

    def rpc_method(self,method,ex_service,**kwargs):
        """
        统一调用方法
        method : query,item,find,findone,delete,update,add,top,count
        ex_service : 表名
        """
        #self.table_name = ex_service
        m = getattr(self,method)
        ret = m(yt_mongo_table_name = ex_service,**kwargs)
        return ret

    def db(self):
        raise NotImplementedError(u'请重载')

    def collection(self,table_name):
        raise NotImplementedError(u'请重载')

    def drop(self,yt_mongo_table_name = None):
        """
        删除表
        """
        return self.collection(yt_mongo_table_name).drop()

    def ensure_index(self,item, background=True,yt_mongo_table_name = None):
        """
        增加索引
        """
        return self.collection(yt_mongo_table_name).ensure_index(item, background=background)

    def rename(self, new_name, yt_mongo_table_name=None):
        """
        集合重命名
        :param new_name:
        :param yt_mongo_table_name:
        :return:
        """
        return self.collection(yt_mongo_table_name).rename(new_name)

    def query(self,where,sort,page,per_page,yt_mongo_table_name = None):
        query = self.collection(yt_mongo_table_name).find(where)
        if sort and sort != []:
            query = query.sort(sort)

        length = query.count()
        if (page - 1) * per_page > length : page = 1
        return {'l':length,
                'd':list(query.skip((page - 1) * per_page).limit(per_page))}

    def item(self,id,yt_mongo_table_name = None):
        return self.collection(yt_mongo_table_name).find_one({'_id':id})

    def find(self, query, sort=None, select=None, yt_mongo_table_name = None):
        if select:
            query = self.collection(yt_mongo_table_name).find(query, select)
        else:
            query = self.collection(yt_mongo_table_name).find(query)
        if sort:
            query = query.sort(sort)
        return list(query)

    def findone(self, query, select, yt_mongo_table_name=None):
        if not select:
            return self.collection(yt_mongo_table_name).find_one(query)
        else:
            return self.collection(yt_mongo_table_name).find_one(query, select)

    def delete(self,id,yt_mongo_table_name = None):
        self.collection(yt_mongo_table_name).remove({'_id':id})

    def update(self,id,yt_mongo_table_name = None,**items):
        self.collection(yt_mongo_table_name).update({'_id':id},{'$set':items})

    def upcmd(self, where, update, upsert=True, multi=True,  yt_mongo_table_name=None, safe=None):
        """
        执行更新命令
        :param where:要更新的数据
        :param update: 要更新的相关数据
        :param upsert: 如果数据不存在的话是否新增
        :param muti: 是更新查到的第一条还是更新所有查到的数据
        :param yt_mongo_table_name: 集合名
        :return:
        """
        if safe:
            self.collection(yt_mongo_table_name).update(where, update, upsert, multi, w='1')
        else:
            self.collection(yt_mongo_table_name).update(where, update, upsert, multi)

    def mupdate(self,where,yt_mongo_table_name = None,**items):
        self.collection(yt_mongo_table_name).update(where,{'$set':items})

    def add(self,yt_mongo_table_name = None,**items):
        return self.collection(yt_mongo_table_name).insert(items)

    def save(self,yt_mongo_table_name = None,**items):
        return self.collection(yt_mongo_table_name).save(items)

    def minsert(self, items, yt_mongo_table_name=None):
        """
        批量写入
        :param items:
        :param yt_mongo_table_name:
        :return:
        """
        return self.collection(yt_mongo_table_name).insert(items)
    def mremove(self, where, yt_mongo_table_name=None):
        """
        根据条件批量删除
        :param items:
        :param yt_mongo_table_name:
        :return:
        """
        return self.collection(yt_mongo_table_name).remove(where)

    def top(self,where ,sort,nums = 10,skip = 0,yt_mongo_table_name = None):
        query = self.collection(yt_mongo_table_name).find(where).sort(sort)
        if skip > 0: query = query.skip(skip)
        return list(query.limit(nums))


    def count(self,query,yt_mongo_table_name = None):
        return self.collection(yt_mongo_table_name).find(query).count()


    def aggregate_s(self, where, yt_mongo_table_name):
        """
        聚合的原始方法
        :param where:
        :param yt_mongo_table_name:
        :return:
        """
        ret = self.collection(yt_mongo_table_name).aggregate(where)
        if type(ret) == dict:
            return ret

        ret = list(ret)

        return {"ok": True, "result": ret}

    def aggregate(self, where, top=None, skip=None, unwind=None, yt_mongo_table_name=None):
        """
        聚合
        :param where:
        :param yt_mongo_table_name:
        :return:
        """
        if top:
           where.append({'$limit': top})
        if skip:
            where.append({'$skip': skip})
        if unwind:
            where.insert(0, {'$unwind': unwind})


        return self.aggregate_s(where=where, yt_mongo_table_name=yt_mongo_table_name)

    def distinct(self, key_name, where, yt_mongo_table_name=None):
        """
        计算去重复之后的结果
        :param where:
        :param yt_mongo_table_name:
        :return:
        """
        ret = self.collection(yt_mongo_table_name).find(where).distinct(key_name)
        return ret

    def collection_names(self):
        """
        获取所有集合名字
        :return:
        """
        return self.db().collection_names()

    def command(self, cmd, **kwargs):
        """
        执行相关命令
        :param cmd:
        :param yt_mongo_table_name:
        :param kwargs:
        :return:
        """
        return self.db().command(cmd, **kwargs)