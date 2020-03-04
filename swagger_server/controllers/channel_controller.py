import connexion
from sqlalchemy.exc import SQLAlchemyError

from swagger_server.models.all_channels import AllChannels  # noqa: E501
from swagger_server.models.channel import Channel  # noqa: E501
from ..models.db_models.channel import Channel as dbChannel
from sqlalchemy.sql import select


def add_channel(body=None):  # noqa: E501
    """Channel has been created

    Channel has been created # noqa: E501

    :param body: The Channel to be create
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Channel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_channel_by_id(id):  # noqa: E501
    """Deletes an existing channel

    Deletes an existing channel # noqa: E501

    :param id: The channel ID
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def get_all_channels():  # noqa: E501
    """Returns all channels

    Returns all channels in a server # noqa: E501


    :rtype: AllChannels
    """
    try:
        # Query DB
        query = dbChannel.query.all()
        response = []
        # Loop through query results and build channel objects for response
        for channel in query:
            c = Channel()
            c.id = channel.channel_id
            c.name = channel.channel_name
            c.capacity = channel.channel_capacity
            c.type = channel.channel_type
            c.position = channel.channel_position
            response.append(c)
        # Return all channels
        res = AllChannels.from_dict(response)
        return res, 200
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


def get_channel_by_id(id):  # noqa: E501
    """Get a channel by its ID

    Returns a single Channel if it exists # noqa: E501

    :param id: The channel ID
    :type id: int

    :rtype: Channel
    """
    return 'do some magic!'


def update_channel_by_id(id, body=None):  # noqa: E501
    """Updates an existing channel

    Updates an existing channel # noqa: E501

    :param id: The channel ID
    :type id: int
    :param body: Channel to be added
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Channel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
