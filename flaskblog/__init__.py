from flask import Flask, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import ProductionConfig, DevelopmentConfig
from dotenv import load_dotenv
from tests.mongo_db import MongoDB

from flask_sslify import SSLify
import os

load_dotenv()
db_name = "db_test"
db = MongoDB(db_name)

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

@login_manager.unauthorized_handler
def unauthorized_callback():
    abort(404)


def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)

    if os.getenv('ENV') == 'development':
        config_class = DevelopmentConfig
    elif os.getenv('ENV') == 'production':
        config_class = ProductionConfig

    app.config.from_object(config_class)
    app.static_folder = 'static'
    #db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    if 'DYNO' in os.environ:
        sslify = SSLify(app)

    return app
