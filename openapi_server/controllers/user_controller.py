import json

import bcrypt
import connexion
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from openapi_server.__main__ import db
from openapi_server.models import db_models
from openapi_server.models.user import User  # noqa: E501
from openapi_server.util import ErrorResponse


def create_user(user):  # noqa: E501
    """Create a User

    Creates a new instance of a User. # noqa: E501

    :param user: A new User to be created.
    :type user: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        try:
            payload = connexion.request.get_json()

            if all(filter(lambda k: k in payload, ['id', 'name', 'password'])):
                u = db_models.User(id=payload['id'],
                                   name=payload['name'],
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


def delete_user(user_id):  # noqa: E501
    """Delete a User

    Deletes an existing User. # noqa: E501

    :param user_id: A unique identifier for a User.
    :type user_id: str

    :rtype: None
    """

    user = db_models.User.query.filter_by(id=user_id).first()
    if user is None:
        return ErrorResponse(404, 'User not found')
    else:
        db.session.delete(user)
        db.session.commit()
        return Response(status=204, mimetype="application/json")


def get_user(user_id):  # noqa: E501
    """Get a User

    Gets the details of a single instance of a User. # noqa: E501

    :param user_id: A unique identifier for a User.
    :type user_id: str

    :rtype: User
    """
    user = db_models.User.query.filter_by(id=user_id).first()
    if user is None:
        return ErrorResponse(404, 'User not found')

    return Response(response=json.dumps(User(id=user.id, name=user.name).to_dict()), status=200, mimetype="application/json")


def get_users():  # noqa: E501
    """List All users

    Gets a list of all User entities. # noqa: E501


    :rtype: List[User]
    """
    try:
        query = db_models.User.query.all()

        response = [User(u.id, u.name).to_dict() for u in query]
        return Response(response=json.dumps(response), status=200, mimetype="application/json")
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return ErrorResponse(500, 'Unable to fetch Users')


def update_user(user_id, user=None):  # noqa: E501
    """Update a User

    Updates an existing User. # noqa: E501

    :param user_id: A unique identifier for a User.
    :type user_id: str
    :param user: Updated User information.
    :type user: dict | bytes

    :rtype: None
    """
    user = db_models.User.query.filter_by(id=user_id).first()

    if connexion.request.is_json:
        if user is None:
            return ErrorResponse(404, 'User not found')
        else:
            u = User.from_dict(connexion.request.get_json())  # noqa: E501

            try:
                print(u)
                for attr in ('id', 'name'):
                    setattr(user, attr, getattr(u, attr))
                print(u)

                db.session.commit()
                return Response(status=204)

            except SQLAlchemyError:
                db.session.rollback()
                return ErrorResponse(500, 'Unable to update channel')

    return ErrorResponse(400, 'Malformed request')
