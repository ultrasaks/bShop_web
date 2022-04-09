from flask import Blueprint, render_template, request, abort
from . import db
from flask_login import current_user, login_required
from .models import App
from werkzeug.exceptions import HTTPException


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@login_required
@main.route('/profile')
def profile():
    return render_template('profile.html')


@main.route('/app/<id>')
def get_app(id):
    app = App.query.filter_by(id=id).first()
    if not app:
        abort(404)
    if not app.is_published:
        if current_user.is_anonymous or current_user.id != app.publisher:
            abort(403)
    return render_template('app.html', app=app)


@main.app_errorhandler(Exception)
def error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    if code == 500:
        print(e)
        e = 'Internal server error'
    return render_template('errors/404.html', code=code, e=e)