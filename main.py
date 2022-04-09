from flask import Blueprint, render_template, request, url_for
from flask import redirect

from .models import App
from . import db
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@login_required
@main.route('/profile')
def profile():
    return render_template('profile.html')


@login_required
@main.route('/createapp', methods=['POST'])
def create_post_app():
    app = App()

    app.name = request.form.get('name')
    app.description = request.form.get('description')
    app.publisher = current_user.id
    app.version = request.form.get('version')
    app.tags = request.form.get('tags')
    app.screenshots = request.form.get('screenshots')
    app.big_icon = request.form.get('big_icon')
    app.small_icon = request.form.get('small_icon')
    app.is_published = False
    db.session.add(app)
    db.session.commit()

    return redirect(url_for('main.index'))


@login_required
@main.route('/createapp')
def create_app():
    return render_template('createapp.html')
