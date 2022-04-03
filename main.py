from flask import Blueprint, render_template, request
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
