from flask import (
    Blueprint, render_template, jsonify, request,
    flash, abort, url_for, redirect
)
from flaskext.uploads import (
    UploadSet, IMAGES, configure_uploads
)
from xmn_flask.views import home
from xmn_flask import app


mod = Blueprint('upload', __name__, url_prefix='/upload')

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

@mod.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        #rec = Photo(filename=filename, user=g.user.id)
        #rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=filename))
    return render_template('upload.html')


@mod.route('/photo/<id>')
def show(id):
    #photo = Photo.load(id)
    filename = '/tmp/photos/%s' % id
    photo = open(filename)
    if photo is None:
        abort(404)
    url = photos.url(filename)
    return render_template('show.html', url=url, photo=photo)