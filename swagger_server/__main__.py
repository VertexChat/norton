#!/usr/bin/env python3
"""
Norton Main Runner
Authors: Cathal Butler, Morgan Reilly

This class handles:
    Database Connection
    Swagger Implementation
"""
import connexion
import config

from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from swagger_server import encoder
# https://stackoverflow.com/questions/10572498/importerror-no-module-named-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# https://flask-login.readthedocs.io/en/latest/
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
database = SQLAlchemy()  # Database connection


# login_manager = LoginManager()  # Get a handle on the Login Manager


def main():
    """Note: pythonic_params (line 33) is used for... """
    connexion_app = connexion.App(__name__, specification_dir='./swagger/')  # Get a handle on the connexion app
    CORS(connexion_app.app)  # Added to allow CORS
    connexion_app.app.json_encoder = encoder.JSONEncoder  # Get a handle on the encoder type ==> JSON
    # validate_responses=True
    connexion_app.add_api('swagger.yaml', arguments={'title': 'Norton API'},
                          pythonic_params=True)  # Set the  connexion api parameters
    connexion_app.app.config.from_object(config.Config)  # Import config file
    try:
        database.init_app(connexion_app.app)  # Initiate database and login manager
    except SQLAlchemyError as e:
        print(e)

    # Database Setup
    with connexion_app.app.app_context():
        # Create all tables from existing database
        # This also generates the engine to connect to for the database,
        # rather than calling it per query in the controller
        database.create_all()

    # Run application
    connexion_app.run(port=8080)


if __name__ == '__main__':
    main()
