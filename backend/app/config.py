import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URL_LOCAL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    TESTING = os.environ.get('FLASK_TESTING') == '1'

class DevelopmentConfig(Config):
    DEBUG = True