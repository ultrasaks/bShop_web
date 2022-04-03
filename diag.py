from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import App, User
from flask_login import current_user, login_required

diag = Blueprint('diag', __name__, url_prefix='/admin')


def is_admin(cu):
    if cu.is_authenticated:
        if cu.is_admin:
            return True
    return False


@diag.route('/components')
def components():
    return render_template('components.html')


@login_required
@diag.route('/')
def admin_panel():
    if not is_admin(current_user):
        return redirect(url_for('main.index'))
    return render_template('admin/adminbase.html')


@login_required
@diag.route('/users')
def users():
    if not is_admin(current_user):
        return redirect(url_for('main.index'))
    users_list = User.query.order_by(User.id)
    return render_template('admin/users.html', users_list=users_list)


@login_required
@diag.route('/user')
def get_user():
    if not is_admin(current_user):
        return redirect(url_for('main.index'))
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    return render_template('admin/getuser.html', user=user)


@login_required
@diag.route('/user', methods=['POST'])
def post_user():
    if not is_admin(current_user):
        return redirect(url_for('main.index'))
    user_id = request.args.get('id')
    user = User.query.get(user_id)

    user.name = request.form.get('name')
    user.email = request.form.get('email')
    user.apps = eval(request.form.get('apps'))
    user.favourites = eval(request.form.get('favourites'))
    user.is_admin = True if request.form.get('is_admin') else False
    user.is_banned = True if request.form.get('is_banned') else False
    db.session.add(user)
    db.session.commit()

    return render_template('admin/getuser.html', user=user)
