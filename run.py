from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from app import create_app

app = create_app("config.cfg")
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


if __name__ == '__main__':
    manager.run()
