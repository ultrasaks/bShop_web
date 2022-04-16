from flask import Blueprint, render_template, request, redirect, url_for, abort
from . import db
from .models import App, User
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')


def is_admin(cu):
    if cu.is_authenticated:
        if cu.is_admin:
            return True
    return False


@admin.route('/components')
def components():
    apps = App.query.order_by(App.id.desc())[:2]
    return render_template('info/components.html', title='Components test', apps=apps)


@admin.route('/')
@login_required
def admin_panel():
    if not is_admin(current_user):
        abort(403)
    return render_template('admin/adminbase.html', title='Admin')


@admin.route('/users')
@login_required
def users():
    if not is_admin(current_user):
        abort(403)
    users_list = User.query.order_by(User.id)
    return render_template('admin/users.html', users_list=users_list, title='Users')


@admin.route('/user')
@login_required
def get_user():
    if not is_admin(current_user):
        abort(403)
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    return render_template('admin/getuser.html', user=user, title=user.name)


@admin.route('/apps')
@login_required
def apps():
    if not is_admin(current_user):
        abort(403)
    apps_list = App.query.order_by(App.id)
    return render_template('admin/apps.html', apps_list=apps_list, title='Apps')


@admin.route('/unreviewed')
@login_required
def unreviewed():
    if not is_admin(current_user):
        abort(403)
    apps_list = App.query.order_by(App.id).filter_by(is_published=False)
    return render_template('admin/unreviewed.html', apps_list=apps_list, title='Unreviewed')



@admin.route('/app')
@login_required
def get_app():
    if not is_admin(current_user):
        abort(403)
    app_id = request.args.get('id')
    app = App.query.get(app_id)
    return render_template('admin/getapp.html', app=app, title='Pre-publish')


@admin.route('/createapp')
@login_required
def create_app():
    if not is_admin(current_user):
        abort(403)
    return render_template('admin/createapp.html', title='Create an app')


# POST-запросы
@admin.route('/app', methods=['POST'])
@login_required
def post_app():
    if not is_admin(current_user):
        abort(403)
    app_id = request.args.get('id')
    app = App.query.get(app_id)

    form = request.form

    app.name = form.get('name')
    app.description = form.get('description')
    app.publisher = form.get('publisher')
    app.publisher_name = form.get('publisher_name')
    app.version = form.get('version')
    app.download_link = form.get('download_link')
    app.weight = form.get('weight')
    app.tags = eval(form.get('tags'))
    app.screenshots = eval(form.get('screenshots'))
    app.huge_icon = form.get('huge_icon')
    app.big_icon = form.get('big_icon')
    app.small_icon = form.get('small_icon')
    app.is_published = True if form.get('is_published') else False
    db.session.add(app)
    db.session.commit()

    return render_template('admin/getapp.html', app=app)


@admin.route('/user', methods=['POST'])
@login_required
def post_user():
    if not is_admin(current_user):
        abort(403)
    user_id = request.args.get('id')
    user = User.query.get(user_id)

    if int(user_id) != 1:
        form = request.form
        user.name = form.get('name')
        user.email = form.get('email')
        user.apps = eval(form.get('apps'))
        user.favourites = eval(form.get('favourites'))
        user.is_admin = True if form.get('is_admin') else False
        user.is_banned = True if form.get('is_banned') else False
        db.session.add(user)
        db.session.commit()

    return render_template('admin/getuser.html', user=user)


@admin.route('/createapp', methods=['POST'])
@login_required
def create_post_app():
    if not is_admin(current_user):
        abort(403)
    app = App()

    form = request.form
    app.name = form.get('name')
    app.description = form.get('description')
    app.publisher = form.get('publisher')
    app.version = form.get('version')
    app.weight = form.get('weight')
    app.tags = eval(form.get('tags'))
    app.screenshots = eval(form.get('screenshots'))
    app.big_icon = form.get('big_icon')
    app.small_icon = form.get('small_icon')
    app.is_published = True if form.get('is_published') else False
    db.session.add(app)
    db.session.commit()

    return render_template('admin/getapp.html', app=app)


@admin.route('/delete')
@login_required
def delete_app():
    if not is_admin(current_user):
        abort(403)
    app_id = request.args.get('id')
    app = App.query.get(app_id)
    if app:
        db.session.delete(app)
        db.session.commit()
    return redirect('/admin')