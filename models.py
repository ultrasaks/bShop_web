from flask_login import UserMixin
from . import db, create_app
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    apps = db.Column(db.JSON, default=[])
    favourites = db.Column(db.JSON, default=[])

    def short_mail(self):
        if len(self.email) > 30:
            return f'{self.email[:30]}...'
        return self.email

    def short_name(self):
        if len(self.name) > 30:
            return f'{self.name[:30]}...'
        return self.name

    def len_app(self):
        return len(self.apps)


class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(3000))
    date_published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    publisher = db.Column(db.Integer)
    version = db.Column(db.String(10))
    weight = db.Column(db.String(20))
    tags = db.Column(db.JSON)
    screenshots = db.Column(db.JSON)
    big_icon = db.Column(db.String(200))
    small_icon = db.Column(db.String(200))
    download_link = db.Column(db.String(3000))
    is_published = db.Column(db.Boolean, default=False)
    downloads = db.Column(db.Integer, default=0)
