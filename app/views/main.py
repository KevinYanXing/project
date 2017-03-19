from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/user/', methods=['GET', 'POST'])
def user():
    pass