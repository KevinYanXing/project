# coding=utf-8
from wtforms.fields import DateField
from time import mktime,strptime

class SDateField(DateField):
    """
    文本框组件
    """

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = mktime(strptime(date_str, '%Y-%m-%d'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('You may input a fake date =.=!'))
