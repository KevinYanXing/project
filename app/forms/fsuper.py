# coding=utf-8
from wtforms.fields import DateField
from wtforms.form import Form
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

class SPhoneField(DateField):
    """
    电话号码
    """

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = mktime(strptime(date_str, '%Y-%m-%d'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('You may input a fake date =.=!'))

# class BaseForm(Form):
#
#     button_text = u'submit'
#
#     isTop = True
#
#     def __init__(self, template=None, **kwargs):
#         self.template = template
#         self.kwargs = kwargs
#         self.obj = self.item()
#         # 自动处理表单数据
#         if self.is_submitted:
#             formdata = request.form
#             if request.files:
#                 formdata = formdata.copy()
#                 formdata.update(request.files)
#             elif request.json:
#                 formdata = werkzeug.datastructures.MultiDict(request.json)
#         else:
#             formdata = None
#
#         super(BaseForm, self).__init__(formdata=formdata, obj=self.obj, **kwargs)
#
#
#     def item(self):
#         """
#         根据请求的URL参数获取单条数据，这个方法如果需要的话请重载。
#         一般在修改数据的时候才需要这个方法有返回
#         如果不是修改，新增的时候，根据URL参数判断是否带有ID，如果不带又ID直接返回None
#         只有在非提交数据的时候才会请求这个方法
#         从这个方法得到数据后，会自动将同名属性赋值到表单项中
#         :return:
#         """
#         return None
#
#     def submit(self):
#         """
#         一定要重载此方法,用于表单提交成功后的操作
#         成功，直接返回跳转到的地址
#         失败，返回None或者False
#         成功失败信息都字节写入flash里面即可
#         :return:
#         """
#         raise NotImplementedError(u'请重载表单的submit方法')
#
#     def run(self, **kwargs):
#         """
#         全局调用执行，根据是submit还是普通来返回
#         :return:
#         """
#         if self.is_submitted:
#             if not self.validate():
#                 return self._valid_error()
#
#             ret = self.submit()
#             if not ret:
#                 return self._submit_error()
#
#             return self._submit_ok(ret)
#         else:
#             return self.render(**kwargs)
#
#     def render(self, **kwargs):
#         """
#         返回响应内容
#         """
#         if not self.template:
#             template = request.endpoint.replace('.', '/') + '.html'
#         else:
#             template = self.template
#
#         kwargs['form'] = self
#
#         return Help.render(template, **kwargs)
#
#
#     def _submit_ok(self, url):
#         """
#         执行成功后，跳转到URL
#         """
#         if url.find('submit_') == 0:
#             return self._show_submit_finish({'params': url[7:]}, 'submit_finish')
#
#         return self._show_submit_finish({'url': url}, 'redirect')
#
#     def _submit_error(self):
#         """
#         返回flash里面的
#         """
#         msgs = get_flashed_messages(with_categories=True)
#         err = {}
#         for k, v in msgs:
#             if k not in err.keys():
#                 err[k] = [v]
#             else:
#                 err[k].append(v)
#         return self._show_submit_finish(err, 'errors')
#
#     def _valid_error(self):
#         """
#         返回JS代码
#         """
#         err = dict()
#         for field in self:
#             if field.errors:
#                 for error in field.errors:
#                     err[field.name] = unicode(error)
#                     if _is_hidden(field):
#                         err[field.name + '__hidden'] = True
#         # 将这个err通过调用指定的JS方法实现
#         return self._show_submit_finish(err, 'validate')
#
#     def _show_submit_finish(self, val, method):
#         """
#         输出JS响应
#         :param val:
#         :param method:
#         :return:
#         """
#
#         if method == 'validate' or self.isTop:
#             val = json.dumps(val)
#             val = 'top.DAMY.loader.%s(%s);' %(method, val)
#         else:
#             val['me'] = True
#             val = json.dumps(val)
#             val = 'parent.DAMY.loader.%s(%s);' %(method, val)
#
#         val = '<html><head><noscript><meta http-equiv="refresh" content="0;url=about:noscript"></noscript><script type="text/javascript">%s</script></head></html>' %val
#         return Markup(val)
#
#     @property
#     def is_submitted(self):
#         """
#         检查是不是表单提交的操作
#         """
#         return request and request.method in ("PUT", "POST")
#
#
#     def form(self, id=None, action='', target='__hidden_call', **kwargs):
#         """
#         在HTML页面中调用此方法来实现form标签的render
#         """
#         form_name = type(self).__name__
#         if not id:
#             id = form_name
#         result = []
#         result.append(u'<form action="')
#         result.append(action)
#         result.append(u'" method="post" class="ajax_form" onsubmit="DAMY.loader.submit(this);" target="'+target+ u'" data-bind="ajax_form" id="')
#         result.append(id)
#         result.append(u'_form" name="')
#         result.append(form_name)
#         result.append(u'_form"')
#         for k, v in kwargs.items():
#             result.append(' '+k+'="' + v + '"')
#         result.append(u'>')
#
#
#         return Markup(u"".join(result))
