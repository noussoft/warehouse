import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False

    CSRF_ENABLED = True

    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WHOOSH_BASE = os.path.join(basedir, 'search.db')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True