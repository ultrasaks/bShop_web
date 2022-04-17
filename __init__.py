from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5cd80b4bcb0af7e2f81ffa01138e85fd9ae01c9dd8d3d480a8c552925f25'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['CAPTCHA_ENABLE'] = True
    app.config['CAPTCHA_LENGTH'] = 5
    app.config['CAPTCHA_WIDTH'] = 160
    app.config['CAPTCHA_HEIGHT'] = 60
    app.config['SESSION_TYPE'] = 'sqlalchemy'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .admin import admin as diag_blueprint
    from .apps import apps as apps_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(diag_blueprint)
    app.register_blueprint(apps_blueprint)

    Session(app)
    captcha = FlaskSessionCaptcha(app)

    migrate = Migrate(app, db)

    app.logger.handlers.clear()

    return app


app = create_app()

