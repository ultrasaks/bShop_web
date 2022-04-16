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


@apps.route('/')
@login_required
def library():
    apps_list = []
    for app_id in current_user.library:
        apps_list.append(App.query.get(app_id))
    return render_template('apps/library.html', title='Library', apps_list=apps_list)


@apps.route('/uploaded')
@login_required
def my_apps():
    apps_list = App.query.filter_by(publisher=current_user.id)
    return render_template('apps/myapps.html', title='My apps', apps_list=apps_list)


@apps.route('/createapp', methods=['POST'])
@login_required
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
    app.huge_icon = form.get('huge_icon')
    app.big_icon = form.get('big_icon')
    app.small_icon = form.get('small_icon')
    app.download_link = form.get('download_link')
    app.publisher_name = current_user.name
    platform = form.get('platform')
    if platform != '0' and platform != '1':
        platform = '0'
    app.platform = int(platform)
    db.session.add(app)
    db.session.commit()

    return redirect(url_for('main.index'))


@apps.route('/createapp')
@login_required
def create_app():
    return render_template('apps/createapp.html', title='Publish an app')


@apps.route('/app/<app_id>')
def get_app(app_id):
    app = App.query.filter_by(id=app_id).first()
    if not app:
        abort(404)
    if not app.is_published:
        if current_user.is_anonymous or current_user.id != app.publisher:
            abort(403)
    return render_template('apps/app.html', app=app, title=app.name)


@apps.route('/add/<app_id>')
@login_required
def add_to_library(app_id):
    user = User.query.get(current_user.id)
    q = user.library.copy()
    app = App.query.get(int(app_id))
    if int(app_id) not in user.library:
        if app and app.is_published:
            q.append(int(app_id))
            app.downloads += 1
    else:
        q.remove(int(app_id))
        app.downloads -= 1
    user.library = q
    db.session.add(user)
    db.session.add(app)
    db.session.commit()
    return_to = request.args.get('return_to')
    if return_to is None:
        return_to = f'/apps/app/{app_id}'
    return redirect(return_to)


@apps.route('/list/<type>')
@login_required
def applist(type):
    return 0