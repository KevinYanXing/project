# coding=utf-8
from time import mktime
from flask import render_template,current_app
from datetime import datetime

class Help:
    def __init__(self):
        pass

    @staticmethod
    def render(template, **kwargs):
        kwargs['help'] = Help
        return render_template(template, **kwargs)

    @staticmethod
    def split(val, sp):
        if not val:
            return []
        return val.split(sp)

    @staticmethod
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
        try:
            ret = ts.strftime(format)
        except:
            return ts

        return ret.decode('utf-8')

    @staticmethod
    def str_to_ts(val, formate='%Y-%m-%d %H:%M:%S'):
        """
        将文本时间转换成时间戳
        """
        tmp = datetime.strptime(val, formate)
        return mktime(tmp.timetuple())

    @staticmethod
    def format_float(val):
        return float('%.2f' % val)

    @staticmethod
    def for_index(arr):
        return enumerate(arr)

    @staticmethod
    def format_content(val):
        print val
        val = val.replace('\n','<br>')
        return val

