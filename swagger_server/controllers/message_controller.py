import connexion
import six

from swagger_server.models.all_messages import AllMessages  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.message import Message  # noqa: E501
from swagger_server import util


def add_message(body=None):  # noqa: E501
    """Message has been created

    Message has been created # noqa: E501

    :param body: Message to be added
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Message.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_message_by_id(id):  # noqa: E501
    """Deletes an existing message

    Deletes an existing message # noqa: E501

    :param id: The message ID
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def get_all_messages():  # noqa: E501
    """Returns all messages

    Returns all messages in a channel # noqa: E501


    :rtype: AllMessages
    """
    return 'do some magic!'


def get_message_by_id(id):  # noqa: E501
    """Get a message by its ID

    Returns a single message if it exists # noqa: E501

    :param id: The message ID
    :type id: int

    :rtype: Message
    """
    return 'do some magic!'


def update_message_by_id(id, body=None):  # noqa: E501
    """Updates an existing message

    Updates an existing message # noqa: E501

    :param id: The message ID
    :type id: int
    :param body: Message to be added
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Message.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
