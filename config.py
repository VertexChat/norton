import os
import uuid


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # FLASK_APP = os.environ.get('FLASK_APP')
    # FLASK_ENV = os.environ.get('FLASK_ENV')
    DEBUG = False
    CSRF_ENABLED = True
   # SECRET = os.environ.getenv('SECRET', 'default_secret_key')
    # Database
    DEFAULT_URI = 'mysql://root:root@172.17.0.2/vertex_db'
    SQLALCHEMY_DATABASE_URI = DEFAULT_URI
    NOTIFICATION_SERVICE_AUTHKEY = b'7qH4vt@@rC*qLAVZegrRe@Nx'
