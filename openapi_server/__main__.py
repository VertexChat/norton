#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
import connexion
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

import config
from openapi_server import encoder

db = SQLAlchemy()


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    # CORS(app.app, supports_credentials=True, origin="http://localhost:36859/")  # Added to allow CORS
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Norton'}, pythonic_params=True)

    app.app.config.from_object(config.Config)

    try:
        db.init_app(app.app)
    except SQLAlchemyError as e:
        print(e)

    with app.app.app_context():
        db.create_all()
    app.run(port=8080)


if __name__ == '__main__':
    main()
