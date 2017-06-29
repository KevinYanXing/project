# -*- coding: utf-8 -*-
from redis import Redis as RedisClass
# import inspect
# import urlparse
# from werkzeug.utils import import_string


class DRedis(object):
    """
    基于redis的封装，便于配置文件配置
    """
    # converters = {'port': int}

    def __init__(self, app=None, config_prefix=None, db=None, idx=0):
        """
        Constructor for non-factory Flask applications
        """
        if app is not None:
            self.init_app(app, config_prefix, db, idx)

    # def _convert(self, arg, val):
    #     """
    #     Apply a conversion method to specific arguments i.e. ports
    #     """
    #     return self.converters[arg](val) if arg in self.converters else val
    #
    # def _get_connection_class_args(self, c):
    #     """
    #     Returns the args that are expected by the Redis class
    #     """
    #     return ([a.upper() for a in inspect.getargspec(c.__init__).args
    #             if a != 'self'])

    # def _parse_configuration(self, url=None):
    #     """
    #     Parse the configuration attached to our application. We provide
    #     URL as a default, and other set values (including URL) will override
    #     the defaults that are parsed.
    #     """
    #     if url:
    #         urlparse.uses_netloc.append('redis')
    #         url = urlparse.urlparse(url)
    #
    #         self.app.config[self.key('HOST')] = url.hostname
    #         self.app.config[self.key('PORT')] = url.port or 6379
    #         self.app.config[self.key('USER')] = url.username
    #         self.app.config[self.key('PASSWORD')] = url.password
    #         db = url.path.replace('/', '')
    #         self.app.config[self.key('DB')] = db if db.isdigit() else 0
    #
    #     host = self.app.config.get(self.key('HOST'), '')
    #
    #     if host.startswith('file://') or host.startswith('/'):
    #         self.app.config.pop(self.key('HOST'))
    #         self.app.config[self.key('UNIX_SOCKET_PATH')] = host

    # def _generate_connection_kwargs(self, args):
    #     """
    #     Generates the kwargs for the Redis class
    #     """
    #
    #     def value(arg):
    #         """
    #         Returns the value of the argument from the application config
    #         """
    #         return self._convert(arg, self.app.config[self.key(arg)])
    #
    #     args = [arg for arg in args if self.key(arg) in self.app.config]
    #     return dict([(arg.lower(), value(arg)) for arg in args])

    def init_app(self, app, key='REDIS_', db=None, idx=0):
        """
        Apply the Flask app configuration to a Redis object
        """
        self.app = app

        setting = self.app.config.get(key + 'URL')
        if type(setting) == list:
            setting = setting[idx]

        self.connection = connection = RedisClass.from_url(setting, db=db)
        self._include_connection_methods(connection)

    def _include_connection_methods(self, connection):
        """
        Include methods from connection instance to current instance.
        """
        for attr in dir(connection):
            value = getattr(connection, attr)
            if attr.startswith('_') or not callable(value):
                continue
            self.__dict__[attr] = value
