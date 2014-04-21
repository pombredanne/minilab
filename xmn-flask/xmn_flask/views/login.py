from flask import Blueprint, render_template, jsonify, request
from xmn_flask.views import home

mod = Blueprint('login', __name__, url_prefix='/login')


def valid_login(u, p):
    return True


def log_the_user_in(name):
    return home.hello(name)


@mod.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@mod.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(
                request.args.get('username', ''),
                request.args.get('password', '')
        ):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login/login.html', error=error)