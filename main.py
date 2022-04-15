from flask import Blueprint, render_template, request, abort, redirect, url_for
from . import db
from flask_login import current_user, login_required
from .models import App
from werkzeug.exceptions import HTTPException

main = Blueprint('main', __name__)


@main.route('/')
def index():
    new_apps = App.query.order_by(App.id.desc()).filter_by(is_published=True)[:2]
    return render_template('index.html', title='Home', new_apps=new_apps)


@login_required
@main.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')


@main.app_errorhandler(Exception)
def error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    if code == 500:
        print(e)
        e = 'Internal server error'
    return render_template('errors/404.html', code=code, e=e, title='Something went wrong')
