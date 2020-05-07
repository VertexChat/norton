import datetime
import json
import time
from multiprocessing.connection import Client
import connexion
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from openapi_server.__main__ import db
from openapi_server.models import db_models
from openapi_server.models.channel import Channel
from openapi_server.models.message import Message
from openapi_server.models.user import User
from openapi_server.util import ErrorResponse


def add_user_to_channel(channel_id, user=None):
    """add_user_to_channel

    :param channel_id: 
    :type channel_id: int
    :param user: 
    :type user: dict | bytes

    :rtype: None
    """

    ch = db_models.Channel.query.filter_by(id=channel_id).first()
    if ch is None:
        return ErrorResponse(404, 'Channel not found')

    if user is None and connexion.request.is_json:
        user = connexion.request.get_json()

    user = db_models.User.query.filter_by(id=user['id']).first()

    if user is None:
        return ErrorResponse(404, 'User not found')

    try:
        query = db.session.query(db_models.t_member).filter(db_models.t_member.c.channel == channel_id).all()

        if user.id in [member.user for member in query]:
            return ErrorResponse(409, 'User is already a member')
        else:
            ch.user.append(user)
            db.session.commit()

            notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
            for _, user_id in query:
                notifier.send({"target": user_id, "type": "add_user_to_channel", "payload": {'user': user.id, 'channel': ch.id}})
            notifier.close()

        return Response(headers={'Location': f'/api/v1/channels/{channel_id}/members/{user.id}'}, status=201)

    except SQLAlchemyError as e:
        db.session.rollback()
        return ErrorResponse(500, 'Internal Server Error')


# TODO: Can args be changed to use channel
def create_channel(channel=None):
    """Create a Channel

    Creates a new instance of a Channel.

    :param channel: A new Channel to be created.
    :type channel: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        try:
            ch = Channel.from_dict(connexion.request.get_json())
            if len(db_models.Channel.query.filter_by(name=ch.name).all()) > 0:
                return ErrorResponse(409, 'A channel already exists with that name')

            channel = db_models.Channel(id=ch.id, name=ch.name, creator_id=100, type=ch.type)

            db.session.add(channel)
            users = db.session.query(db_models.User).all()
            db.session.commit()

            for user in users:
                notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
                notifier.send({"target": user.id, "type": "create_channel", "payload": {'channel': channel.id}})
                notifier.close()

            return Response(headers={'Location': f'/api/v1/channels/{channel.id}'}, status=201)
        except SQLAlchemyError:
            db.session.rollback()
            return ErrorResponse(500, 'Internal Server Error')
    return 'do some magic!'


def create_message(channel_id, message=None):
    """Create a Message

    Creates a new instance of a Message.

    :param channel_id: 
    :type channel_id: int
    :param message: A new Message to be created.
    :type message: dict | bytes

    :rtype: None
    """
    ch = db_models.Channel.query.filter_by(id=channel_id).first()

    if ch is None:
        return ErrorResponse(404, 'Channel not found')
    else:
        m = Message.from_dict(connexion.request.get_json())
        user = None
        with db.engine.connect() as con:
            user = next(con.execute(f"SELECT user FROM session JOIN user u on session.user = u.id;"))[0]

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(m.timestamp))
        message = db_models.Message(channel=channel_id, author=user, content=m.content, timestamp=timestamp)

        try:
            db.session.add(message)
            db.session.commit()
            query = db.session.query(db_models.t_member).filter(db_models.t_member.c.channel == channel_id).all()

            for user_id in [member.user for member in query]:
                notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
                notifier.send({"target": user_id, "type": "create_message", "payload": {'channel': ch.id}})
                notifier.close()
            return Response(headers={'Location': f'/api/v1/channels/{channel_id}/messages/{message.id}'}, status=201)

        except SQLAlchemyError as e:
            db.session.rollback()
            return ErrorResponse(500, 'Internal Server Error')


def delete_channel(channel_id):
    """Delete a Channel

    Deletes an existing Channel.

    :param channel_id: A unique identifier for a Channel.
    :type channel_id: str

    :rtype: None
    """
    try:
        ch = db_models.Channel.query.filter_by(id=channel_id).first()

        if ch is None:
            return ErrorResponse(404, f"Channel '{channel_id}' not found")
        else:
            with db.engine.connect() as con:
                rs = con.execute(f"SELECT * FROM member where channel={ch.id}")
                db.session.delete(ch)

                for _, user_id in rs:
                    notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
                    notifier.send({"target": user_id, "type": "delete_channel", "payload": {'channel': ch.id}})
                    notifier.close()

            db.session.commit()

            return Response(status=204, mimetype="application/json")

    except SQLAlchemyError:
        db.session.rollback()
        return


def delete_message(channel_id, message_id):
    """Delete a Message

    Deletes an existing Message.

    :param channel_id: A unique identifier for a Message.
    :type channel_id: int
    :param message_id: 
    :type message_id: int

    :rtype: None
    """
    ch = db_models.Channel.query.filter_by(id=channel_id).first()
    if ch is None:
        return ErrorResponse(404, 'Channel not found')

    m = db_models.Message.query.filter_by(id=message_id).first()
    if ch is None:
        return ErrorResponse(404, 'Channel not found')

    try:
        db.session.delete(m)
        db.session.commit()
        with db.engine.connect() as con:
            rs = con.execute(f"SELECT * FROM member where channel={ch.id}")

            for _, user_id in rs:
                notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
                notifier.send({"target": user_id, "type": "delete_message", "payload": {'channel': ch.id, 'message': m.id}})
                notifier.close()

        return Response(status=204)

    except SQLAlchemyError:
        return ErrorResponse(404, 'Channel not found')


def get_channel(channel_id):
    """Get a Channel

    Gets the details of a single instance of a Channel.

    :param channel_id: A unique identifier for a Channel.
    :type channel_id: int

    :rtype: Channel
    """
    ch = db_models.Channel.query.filter_by(id=channel_id).first()

    if ch is None:
        return ErrorResponse(404, 'Channel not found')
    else:
        channel = Channel(ch.id, ch.name, ch.type)
        return Response(response=json.dumps(channel.to_dict()), status=200, mimetype="application/json")


def get_channel_members(channel_id):
    """List All members

    Gets a list of all Users in a given Channel.

    :param channel_id: 
    :type channel_id: int

    :rtype: List[User]
    """
    ch = db_models.Channel.query.filter_by(id=channel_id).first()

    if ch is None:
        return ErrorResponse(404, 'Channel not found')
    else:
        query = db.session.query(db_models.User).join(db_models.t_member).join(db_models.Channel).filter(
            db_models.Channel.id == channel_id).all()
        members = [User(u.id, u.name).to_dict() for u in query]
        return Response(response=json.dumps(members), status=200, mimetype="application/json")


def get_channels():
    """List All channels

    Gets a list of all Channel entities.


    :rtype: List[Channel]
    """
    try:
        query = db_models.Channel.query.all()

        # TODO: Currently creator_id is not used is it worth implementing?
        response = [Channel(c.id, c.name, c.type).to_dict() for c in query]
        return Response(response=json.dumps(response), status=200, mimetype="application/json")
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return ErrorResponse(500, 'Unable to fetch Channels')


def get_message(channel_id, message_id):
    """Get a Message

    Gets the details of a single instance of a Message.

    :param channel_id: A unique identifier for a Message.
    :type channel_id: int
    :param message_id: 
    :type message_id: int

    :rtype: Message
    """

    ch = db_models.Channel.query.filter_by(id=channel_id).first()
    if ch is None:
        return ErrorResponse(404, 'Channel not found')

    m = db_models.Message.query.filter_by(id=message_id).first()
    if ch is None:
        return ErrorResponse(404, 'Channel not found')

    # TODO: Converting to Epoch time as database stores timestamp incorrectly. Remove when DB is fixed
    return Response(
        response=json.dumps(Message(m.id, m.channel, m.author, m.content, int(m.timestamp.timestamp()) if type(
            m.timestamp) == datetime.datetime else m.timestamp).to_dict()), status=200,
        mimetype="application/json")


def get_messages(channel_id):
    """List All messages

    Gets a list of all Message entities.

    :param channel_id: 
    :type channel_id: int

    :rtype: List[Message]
    """

    ch = db_models.Channel.query.filter_by(id=channel_id).first()

    if ch is None:
        return ErrorResponse(404, 'Channel not found')
    else:
        query = db_models.Message.query.filter_by(channel=channel_id).all()
        # TODO: Converting to Epoch time as database stores timestamp incorrectly. Remove when DB is fixed
        messages = [Message(m.id, m.channel, m.author, m.content, int(m.timestamp.timestamp()) if type(
            m.timestamp) == datetime.datetime else m.timestamp).to_dict() for m in query]
        return Response(response=json.dumps(messages), status=200, mimetype="application/json")


def remove_channel_member(channel_id, user_id):
    """Remove as User

    Removes a User for a Channel

    :param channel_id: 
    :type channel_id: int
    :param user_id: 
    :type user_id: int

    :rtype: None
    """
    ch = db_models.Channel.query.filter_by(id=channel_id).first()
    if ch is None:
        return ErrorResponse(404, 'Channel not found')

    u = db.session.query(db_models.t_member).join(db_models.User).join(db_models.Channel).filter(db_models.Channel.id == channel_id).first()
    if u is None:
        return ErrorResponse(404, 'User not found in channel')

    try:
        query = db.session.query(db_models.User).join(db_models.t_member).join(db_models.Channel).filter(db_models.Channel.id == channel_id).all()

        db.engine.execute("DELETE FROM member where channel=%(channel)s AND user=%(user)s", {'channel': channel_id, 'user': user_id})
        db.session.commit()

        for user in query:
            notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
            notifier.send({"target": user.id, "type": "remove_channel_member", "payload": {'channel': ch.id, 'message': user_id}})
            notifier.close()

        return Response(status=204)

    except SQLAlchemyError as e:
        print(e)
        return ErrorResponse(404, 'Channel not found')


# TODO: Can args be changed to use channel
def update_channel(channel_id, channel=None):
    """Update a Channel

    Updates an existing Channel.

    :param channel_id: A unique identifier for a Channel.
    :type channel_id: int
    :param channel: Updated Channel information.
    :type channel: dict | bytes

    :rtype: None
    """
    ch = db_models.Channel.query.filter_by(id=channel_id).first()

    if connexion.request.is_json:
        channel = Channel.from_dict(connexion.request.get_json())

        if ch is None:
            return ErrorResponse(404, f"Channel '{channel_id}' not found")
        else:

            try:
                for attr in ('id', 'name', 'type'):
                    setattr(ch, attr, getattr(channel, attr))
                db.session.commit()

                query = db.session.query(db_models.User).join(db_models.t_member).join(db_models.Channel).filter(db_models.Channel.id == channel_id).all()
                for user in query:
                    notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
                    notifier.send({"target": user.id, "type": "update_channel", "payload": {'channel': ch.id}})
                    notifier.close()
                return Response(status=204)

            except SQLAlchemyError:
                db.session.rollback()
                return ErrorResponse(500, 'Unable to update channel')
    return ErrorResponse(500, 'Unable to update channel')


def update_message(channel_id, message_id, message=None):
    """Update a Message

    Updates an existing Message.

    :param channel_id: A unique identifier for a Message.
    :type channel_id: int
    :param message_id: 
    :type message_id: int
    :param message: Updated Message information.
    :type message: dict | bytes

    :rtype: None
    """

    ch = db_models.Channel.query.filter_by(id=channel_id).first()

    if connexion.request.is_json:
        message = Message.from_dict(connexion.request.get_json())
        message.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message.timestamp))


        if ch is None:
            return ErrorResponse(404, f"Channel '{channel_id}' not found")
        else:

            try:
                m = db_models.Message.query.filter_by(id=message_id).first()
                for attr in ('id', 'channel', 'author', 'content', 'timestamp'):
                    setattr(m, attr, getattr(message, attr))
                db.session.commit()
                query = db.session.query(db_models.User).join(db_models.t_member).join(db_models.Channel).filter(
                    db_models.Channel.id == channel_id).all()
                for user in query:
                    notifier = Client(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)
                    notifier.send({"target": user.id, "type": "update_message", "payload": {'channel': ch.id, 'message': message_id}})
                    notifier.close()

                return Response(status=204)

            except SQLAlchemyError as e:
                db.session.rollback()
                return ErrorResponse(500, 'Unable to update message')
    return ErrorResponse(500, 'Unable to update message')
