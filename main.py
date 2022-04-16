from flask import Blueprint, render_template, request, abort, redirect, url_for
from . import db
from flask_login import current_user, login_required
from .models import App
from werkzeug.exceptions import HTTPException

main = Blueprint('main', __name__)


@main.route('/')
def index():
    new_apps = App.query.order_by(App.id.desc()).filter_by(is_published=True)[:5]
    top_apps = App.query.order_by(App.downloads.desc()).filter_by(is_published=True)[:5]
    top_apps_android = App.query.order_by(App.downloads.desc()).filter_by(is_published=True).filter_by(platform=1)[:5]
    return render_template('home/index.html', title='Home', new_apps=new_apps, top_apps=top_apps,
                           top_apps_android=top_apps_android)


@main.route('/search')
@login_required
def search():
    query = request.args.get('query')
    tags = request.args.get('tags')
    platform = request.args.get('platform')
    sort = request.args.get('sort')

    apps_list = App.query.filter_by(is_published=True)
    if query:
        apps_list = apps_list.filter(App.name.contains(query))
    if tags:
        pass
    if platform:
        if platform and platform != '1':
            platform = 0
        pc = True if platform == '0' else False
        android = True if platform == '1' else False

        apps_list = apps_list.filter_by(platform=platform)
    else:
        pc = True
        android = True
    if sort:
        if sort == 0:
            apps_list = apps_list.order_by(App.name)
        elif sort == 1:
            apps_list = apps_list.order_by(App.Downloads.desc())
        else:
            apps_list = apps_list.order_by(App.id.desc())

    return render_template('home/search.html', apps_list=apps_list, query=query, tags=tags, pc=pc, android=android, sort=sort)


@main.route('/search', methods=['POST'])
@login_required
def search_POST():
    query = '?'
    form = request.form

    name = form.get('query')
    tags = form.get('tags')
    pc = form.get('pc')
    android = form.get('android')
    sort = form.get('sort')

    if name:
        query += f'query={name}&'
    if tags:
        query += f'tags={tags}&'
    if not pc or not android:
        if pc:
            query += f'platform=0&'
        else:
            query += f'platform=1&'
    if sort:
        query += f'sort={sort}'
    return redirect(f'/search{query}')


@main.route('/profile')
@login_required
def profile():
    return render_template('account/profile.html', title='Profile')


@main.app_errorhandler(Exception)
def error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    if code == 500:
        print(e)
        e = 'Internal server error'
    return render_template('errors/404.html', code=code, e=e, title='Something went wrong')


@main.route('/copyrights')
def copyrights():
    return render_template('info/copyrights.html', title='Copyrights')


@main.route('/terms')
def terms():
    return render_template('info/terms.html', title='Terms and conditions')