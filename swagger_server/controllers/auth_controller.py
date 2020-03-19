import connexion

from swagger_server.models.login import Login  # noqa: E501
from . import user_controller as user_control
from ..models.db_models.user import User as dbUser  # database
from ..models.user import User  # user

# Our own created authorisation  -- refer to this one

def login(body=None):  # noqa: E501

    """Allows a user that is registered to login

    Allows a user that is register to login to the application # noqa: E501

    :param body: User to be authenticated
    :type body: dict | bytes

    :rtype: None
    """

    if connexion.request.is_json:
        body = Login.from_dict(connexion.request.get_json())  # noqa: E501
        if body.user_name and body.password:
            user = dbUser.query.filter_by(user_name=body.user_name).first()
            if user:
                if user.check_password(password=body.password):
                    userDetails = User(None, user.user_name, None, user.display_name)
                    return userDetails, 202
                else:
                    return 'Password incorrect', 401
            else:
                return 'User does not exist in the database', 401

    # TODO:
    return 'do some magic!'


def register(body=None):  # noqa: E501
    """Allows a user register a new account

    Allow a user register a new account with the server # noqa: E501

    :param body: User to be registered
    :type body: dict | bytes

    :rtype: None
    """
    # Pass the body to the add_user method as it does the same thing
    return user_control.add_user(body)
