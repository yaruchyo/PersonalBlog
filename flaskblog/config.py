import os



class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'fdsfsodifu9c8vsu9dvhzskdfvujsddiofjsv0'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'yaruchyk.o@gmail.com'
    MAIL_PASSWORD = 'Roma2009'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testdb.db'
    ADMIN_HASH_PASS = '$2b$12$stne02QJ1pXkghj7UsV95.qkkjk.ICXo8rbGonUSePOwF7PaA8Hmu'


