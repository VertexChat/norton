from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    DEBUG = False
    CSRF_ENABLED = True

    # Database
    # DEFAULT_URI = 'mysql://root:root@172.17.0.2/vertex_db'  # Local config with docker
    DEFAULT_URI = 'mysql://root:password@localhost/vertex_db'  # Nero config
    SQLALCHEMY_DATABASE_URI = DEFAULT_URI
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Notification System
    NOTIFICATION_SERVICE_AUTHKEY = b'7qH4vt@@rC*qLAVZegrRe@Nx'
