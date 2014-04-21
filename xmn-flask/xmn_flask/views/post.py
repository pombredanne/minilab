from flask import Blueprint, render_template, jsonify

mod = Blueprint('post', __name__, url_prefix='/post')


@mod.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
