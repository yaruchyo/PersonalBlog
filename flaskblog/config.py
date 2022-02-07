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


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):

    DEBUG = True



