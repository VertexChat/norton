from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    # SECRET_KEY = environ.get('SECRET_KEY')
    # FLASK_APP = environ.get('FLASK_APP')
    # FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = False
    CSRF_ENABLED = True
   # SECRET = environ.getenv('SECRET', 'default_secret_key')
    # Database
    DEFAULT_URI = 'mysql://root:root@172.17.0.2/vertex_db'
    SQLALCHEMY_DATABASE_URI = DEFAULT_URI