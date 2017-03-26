# coding=utf-8
__author__ = 'kevin'
from flask import Flask, render_template
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'frontend.signin'

def create_app(cfg):
    app = Flask(__name__)
    app.config.from_pyfile(cfg)
    app.add_url_rule('/<path:filename>', endpoint='static', view_func=app.send_static_file, subdomain='static')
    login_manager.init_app(app)
    configure_blueprints(app)
    configure_errorhandlers(app)
    configure_extensions(app)
    return app

def configure_blueprints(app):
    from app.views.frontend import frontend
    from app.views.main import main
    app.register_blueprint(frontend, url_prefix='')
    app.register_blueprint(main, url_prefix='/main')

def configure_extensions(app):
    from mdb.ext import db
    app.jinja_env.add_extension("jinja2.ext.loopcontrols")
    db.init_app(app, dbs='DBS')


def configure_errorhandlers(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404


    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

