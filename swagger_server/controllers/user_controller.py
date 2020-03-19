import bcrypt
import connexion

from swagger_server.models.user import User  # noqa: E501
from ..models.db_models.user import User as dbUser
from ..__main__ import database


# https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html


def add_user(body=None):  # noqa: E501
    """User has been created

    User has been created # noqa: E501

    :param body: User to be added
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
        existing_user = dbUser.query.filter_by(user_name=body.username).first()
        if existing_user is None:
            print(body.password)
            user = dbUser(user_name=body.username,
                          password=bcrypt.hashpw(body.password.encode('utf8'), bcrypt.gensalt()),
                          display_name=body.display_name)

            database.session.add(user)
            database.session.commit()
            return 201
        else:
            return "Sorry that username already exists in the database", 401

    return 'do some magic!'


def delete_user_by_id(id):  # noqa: E501
    """Deletes an existing User

    Deletes a user from the database # noqa: E501

    :param id: The User ID
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def get_user_by_id(id):  # noqa: E501
    """Returns a single User if it exists

    Returns a single User if it exists # noqa: E501

    :param id: The User ID
    :type id: int

    :rtype: User
    """

    return 'do some magic!'


def update_user_by_id(id, body=None):  # noqa: E501
    """Updates an existing User

    Updates an existing User # noqa: E501

    :param id: The User ID
    :type id: int
    :param body: User entity to be created
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
