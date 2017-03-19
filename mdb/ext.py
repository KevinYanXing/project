# coding=utf-8
from flask import g
from damydb.wmongo import WMongo


def get_current_user():
    if g.identity and hasattr(g.identity, 'user'):
        return g.identity.user
    else:
        return None

db = WMongo()
