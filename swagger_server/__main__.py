#!/usr/bin/env python3

import connexion
from flask_cors import CORS
from swagger_server import encoder
# https://stackoverflow.com/questions/10572498/importerror-no-module-named-sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

# https://flask-login.readthedocs.io/en/latest/
db = SQLAlchemy()


# login_manager = LoginManager()


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    CORS(app.app)  # Added to allow CORS
    app.app.json_encoder = encoder.JSONEncoder
    # validate_responses=True
    app.add_api('swagger.yaml', arguments={'title': 'Norton API'}, pythonic_params=True)
    # Import config
    app.app.config.from_object(config.Config)
    # Init db and login manager
    db.init_app(app.app)
    # login_manager.init_app(app)

    with app.app.app_context():
        # Create tables for our models
        # from .controllers import auth_controller
        # from . import models

        db.create_all()

    # Run application
    app.run(port=8080)


if __name__ == '__main__':
    main()
