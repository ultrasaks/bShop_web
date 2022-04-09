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
    return render_template('components.html')


@login_required
@admin.route('/')
def admin_panel():
    if not is_admin(current_user):
        abort(403)
    return render_template('admin/adminbase.html')


@login_required
@admin.route('/users')
def users():
    if not is_admin(current_user):
        abort(403)
    users_list = User.query.order_by(User.id)
    return render_template('admin/users.html', users_list=users_list)


@login_required
@admin.route('/user')
def get_user():
    if not is_admin(current_user):
        abort(403)
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    return render_template('admin/getuser.html', user=user)


@login_required
@admin.route('/apps')
def apps():
    if not is_admin(current_user):
        abort(403)
    apps_list = App.query.order_by(App.id)
    return render_template('admin/apps.html', apps_list=apps_list)


@login_required
@admin.route('/unreviewed')
def unreviewed():
    if not is_admin(current_user):
        abort(403)
    apps_list = App.query.order_by(App.id).filter_by(is_published=False)
    return render_template('admin/unreviewed.html', apps_list=apps_list)


@login_required
@admin.route('/app')
def get_app():
    if not is_admin(current_user):
        abort(403)
    app_id = request.args.get('id')
    app = App.query.get(app_id)
    return render_template('admin/getapp.html', app=app)

@login_required
@admin.route('/createapp')
def create_app():
    if not is_admin(current_user):
        abort(403)
    return render_template('admin/createapp.html')

# POST-запросы
@login_required
@admin.route('/app', methods=['POST'])
def post_app():
    if not is_admin(current_user):
        abort(403)
    app_id = request.args.get('id')
    app = App.query.get(app_id)

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


@login_required
@admin.route('/user', methods=['POST'])
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




@login_required
@admin.route('/createapp', methods=['POST'])
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



