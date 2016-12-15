import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False

    WTF_CSRF_ENABLED = True

    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WHOOSH_BASE = os.path.join(basedir, 'search.db')

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True