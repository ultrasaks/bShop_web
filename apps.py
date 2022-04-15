from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db, create_app
from .models import App, User
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

apps = Blueprint('apps', __name__, url_prefix='/apps')


# КОЛХОЗ
app = create_app()
Session(app)
captcha = FlaskSessionCaptcha(app)


@login_required
@apps.route('/')
def library():
    apps_list = []
    for app_id in current_user.library:
        apps_list.append(App.query.get(app_id))
    return render_template('apps/library.html', title='Library', apps_list=apps_list)


@login_required
@apps.route('/uploaded')
def my_apps():
    return render_template('apps/myapps.html', title='My apps')


@login_required
@apps.route('/createapp', methods=['POST'])
def create_post_app():
    if not captcha.validate():
        flash('Please pass the captcha first')
        return redirect(url_for('apps.create_app'))
    app = App()
    form = request.form
    app.name = form.get('name')
    app.description = form.get('description')
    app.publisher = current_user.id
    app.version = form.get('version')
    app.tags = form.get('tags').split(',')
    app.screenshots = form.get('screenshots').split(',')
    app.big_icon = form.get('big_icon')
    app.small_icon = form.get('small_icon')
    app.download_link = form.get('download_link')
    app.publisher_name = current_user.name
    db.session.add(app)
    db.session.commit()

    return redirect(url_for('main.index'))


@login_required
@apps.route('/createapp')
def create_app():
    return render_template('createapp.html', title='Publish an app')


@apps.route('/app/<app_id>')
def get_app(app_id):
    app = App.query.filter_by(id=app_id).first()
    if not app:
        abort(404)
    if not app.is_published:
        if current_user.is_anonymous or current_user.id != app.publisher:
            abort(403)
    return render_template('app.html', app=app, title=app.name)


@login_required
@apps.route('/add/<app_id>')
def add_to_library(app_id):
    user = User.query.get(current_user.id)
    q = user.library.copy()
    app = App.query.get(int(app_id))
    if int(app_id) not in user.library:
        if app and app.is_published:
            q.append(int(app_id))
    else:
        q.remove(int(app_id))
    user.library = q
    db.session.add(user)
    db.session.commit()
    return_to = request.args.get('return_to')
    if return_to is None:
        return_to = f'/apps/app/{app_id}'
    return redirect(return_to)
