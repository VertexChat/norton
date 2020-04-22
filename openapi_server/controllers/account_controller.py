import bcrypt
import connexion
import six
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from openapi_server.__main__ import db
from openapi_server.models import db_models
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server.models.inline_object1 import InlineObject1  # noqa: E501
from openapi_server import util
from openapi_server.util import ErrorResponse


def login():  # noqa: E501
    """Log in

    Attempts to log a user in # noqa: E501

    :param inline_object: 
    :type inline_object: dict | bytes

    :rtype: None
    """

    payload = connexion.request.get_json()
    if all(filter(lambda k: k in payload, ['name', 'password'])):
        user = db_models.User.query.filter_by(name=payload['name']).first()
        print(user)

        if bcrypt.checkpw(payload['name'].encode('utf8'), user.password.encode('utf8')):
            return Response(status=201)
        else:
            return ErrorResponse(401, 'Unauthorized')


# TODO: Should repurpose the add_user method
def register():  # noqa: E501
    """Registers User

    Attempts to register a new user # noqa: E501

    :param inline_object1: 
    :type inline_object1: dict | bytes

    :rtype: None
    """
    payload = connexion.request.get_json()

    if all(filter(lambda k: k in payload, ['name', 'password'])):
        try:
            payload = connexion.request.get_json()

            if all(filter(lambda k: k in payload, ['name', 'password'])):
                u = db_models.User(name=payload['name'],
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

