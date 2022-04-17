from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, create_app
from flask_login import login_user, logout_user, current_user
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

auth = Blueprint('auth', __name__)

# КОЛХОЗ
app = create_app()
Session(app)
captcha = FlaskSessionCaptcha(app)


@auth.route('/signup', methods=['POST'])
def signup_post():
    if not captcha.validate():
        flash('Please pass the captcha first')
        return redirect(url_for('auth.signup'))

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    rpassword = request.form.get('rpassword')
    is_agree = request.form.get('is_agree')

    if rpassword != password:
        flash("Passwords doesn't match")
        return redirect(url_for('auth.signup'))
    if email is None or name is None or password is None:
        flash("ты че самый умный")
        return redirect(url_for('auth.signup'))
    if is_agree is None:
        flash('You must accept the terms and conditions to register')
        return redirect(url_for('auth.signup'))
    if len(password) < 6:
        flash('Password must be at least 6 symbols long')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Account with this email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    flash('Now log in to your new accout')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.'))


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('account/login.html', title='Log in')


@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('account/signup.html', title='Sign up')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


