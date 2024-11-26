from flask import Flask, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import ProductionConfig, DevelopmentConfig
from dotenv import load_dotenv
from flaskblog.service_layer.database_repository.mongo_db import MongoDB
from flaskblog.service_layer.storage_repository.filebase_service import FileBaseStorage
import threading
import time
import requests
from flask_sslify import SSLify
import os

load_dotenv()
db_name = "db_test"
db = MongoDB(db_name)
file_storage = FileBaseStorage()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


@login_manager.unauthorized_handler
def unauthorized_callback():
    abort(404)

def call_webpage():
    web_page = os.getenv('WEB_PAGE')
    while True:
        try:
            response = requests.get(web_page)
            print(f"I got the response: {response}")
            # Process the response if needed
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
        time.sleep(10)  # Wait for 10 seconds before the next request

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)

    if os.getenv('ENV') == 'development':
        config_class = DevelopmentConfig
    elif os.getenv('ENV') == 'production':
        config_class = ProductionConfig
        thread = threading.Thread(target=call_webpage)
        #thread.start()


    app.config.from_object(config_class)
    app.static_folder = 'static'
    #db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.routes_layer.users.routes import users
    from flaskblog.routes_layer.posts.routes import posts
    from flaskblog.routes_layer.main.routes import main
    from flaskblog.routes_layer.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # if 'DYNO' in os.environ:
    #     sslify = SSLify(app)

    return app
