from flask import (
    Flask, request, url_for, redirect, render_template,
    flash, session, g, abort
)
from werkzeug import secure_filename
from flask.ext.admin import Admin

# Uploads
# UPLOADED_FILES_ALLOW
# UPLOADED_FILES_DENY
UPLOADS_DEFAULT_DEST = '/tmp/'

app = Flask(
    __name__,
    template_folder='public/templates',
    static_folder='public/static'
)

app.config.from_object(__name__)
app.secret_key = (
    '$K\xda\xf1\xa5\xd7d \x8b\xddI\x94' +
    '\xc1\xb4\xe8\x97\xa6\\I\xec\xc5\xf8\xe8\x9c'
)

#app.run(host='0.0.0.0')

from xmn_flask.views import home, login, post, upload

app.register_blueprint(home.mod)
app.register_blueprint(login.mod)
app.register_blueprint(post.mod)
app.register_blueprint(upload.mod)

admin = Admin(app, name='XMN Flask')
admin.add_view(home.MyView(name='Home Admin'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)