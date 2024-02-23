from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from configs.config import Config
from importlib import import_module


## register blueprints
def register_blueprints(app):
    from app.api import blueprint as api_bp
    for module_name in ('home', 'auth', 'user', 'register'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
        app.register_blueprint(api_bp)
    return app


# S
socketio = SocketIO(logger=True, engineio_logger=True)

# database
db = SQLAlchemy()
migrate = Migrate()

# user permissions
login = LoginManager()
login.login_view = 'auth_blueprint.login'
login.login_message = 'Please log in to access this page.'

# send emails
mail = Mail()

# use bootstrap (ui/ux)
bootstrap = Bootstrap()


## application factory
def create_app(config=Config):
    # construct core flask app
    app = Flask(__name__)
    # extend app w/ add-ons
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    socketio.init_app(app)
    app = register_blueprints(app)
    return app
