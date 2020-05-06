import datetime
import time
import uuid

import bcrypt
import connexion
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from openapi_server.__main__ import db
from openapi_server.models import db_models
from openapi_server.util import ErrorResponse


def login(inline_object=None):
    """Log in

    Attempts to log a user in

    :param inline_object: 
    :type inline_object: dict | bytes

    :rtype: None
    """

    payload = connexion.request.get_json()

    if all(filter(lambda k: k in payload, ['username', 'password'])):
        user = db_models.User.query.filter_by(name=payload['username']).first()

        if bcrypt.checkpw(payload['password'].encode('utf8'), user.password.encode('utf8')):
            session_id = str(uuid.uuid4())
            # Cookie will be valid for 86400 seconds i.e. One Day
            expiry = int(time.time()) + 86400

            # Revoke old sessions
            db.engine.execute(f'DELETE FROM session WHERE user={user.id};')

            # Add a new valid session_id
            db.engine.execute(f'INSERT INTO session (id, user, expire_after) VALUE ("{session_id}", {user.id}, {expiry});')
            db.session.commit()

            return Response(
                status=204,
                headers={'Set-Cookie': f'session_id={session_id}; Expires={datetime.datetime.fromtimestamp(expiry).strftime("%c")}'}
            )
        else:
            print(payload)
            return ErrorResponse(401, 'Unauthorized')


def register(inline_object=None):
    """Registers User

    Attempts to register a new user

    :param inline_object:
    :type inline_object: dict | bytes

    :rtype: None
    """
    payload = connexion.request.get_json()

    if all(filter(lambda k: k in payload, ['username', 'password'])):
        try:
            payload = connexion.request.get_json()

            if all(filter(lambda k: k in payload, ['username', 'password'])):
                u = db_models.User(
                    name=payload['username'],
                    password=bcrypt.hashpw(payload['password'].encode('utf8'), bcrypt.gensalt())
                )
                
                db.session.add(u)
                db.session.commit()
                return Response(headers={'Location': f'/api/v1/users/{u.id}'}, status=201)
            else:
                return ErrorResponse(code=400, message="Malformed request")
        except SQLAlchemyError:
            db.session.rollback()
            return ErrorResponse(500, 'Internal Server Error')

    else:
        return ErrorResponse(400, 'Malformed Request')
