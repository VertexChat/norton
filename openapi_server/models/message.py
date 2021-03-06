# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime

from typing import List, Dict

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Message(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, channel=None, author=None, content=None, timestamp=None):  # noqa: E501
        """Message - a model defined in OpenAPI

        :param id: The id of this Message.  # noqa: E501
        :type id: int
        :param channel: The channel of this Message.  # noqa: E501
        :type channel: int
        :param author: The author of this Message.  # noqa: E501
        :type author: int
        :param content: The content of this Message.  # noqa: E501
        :type content: str
        :param timestamp: The timestamp of this Message.  # noqa: E501
        :type timestamp: int
        """
        self.openapi_types = {
            'id': int,
            'channel': int,
            'author': int,
            'content': str,
            'timestamp': int
        }

        self.attribute_map = {
            'id': 'id',
            'channel': 'channel',
            'author': 'author',
            'content': 'content',
            'timestamp': 'timestamp'
        }

        self._id = id
        self._channel = channel
        self._author = author
        self._content = content
        self._timestamp = timestamp

    @classmethod
    def from_dict(cls, dikt) -> 'Message':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Message of this Message.  # noqa: E501
        :rtype: Message
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Message.


        :return: The id of this Message.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Message.


        :param id: The id of this Message.
        :type id: int
        """

        self._id = id

    @property
    def channel(self):
        """Gets the channel of this Message.


        :return: The channel of this Message.
        :rtype: int
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        """Sets the channel of this Message.


        :param channel: The channel of this Message.
        :type channel: int
        """

        self._channel = channel

    @property
    def author(self):
        """Gets the author of this Message.


        :return: The author of this Message.
        :rtype: int
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this Message.


        :param author: The author of this Message.
        :type author: int
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def content(self):
        """Gets the content of this Message.


        :return: The content of this Message.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this Message.


        :param content: The content of this Message.
        :type content: str
        """
        if content is None:
            raise ValueError("Invalid value for `content`, must not be `None`")  # noqa: E501

        self._content = content

    @property
    def timestamp(self):
        """Gets the timestamp of this Message.


        :return: The timestamp of this Message.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Message.


        :param timestamp: The timestamp of this Message.
        :type timestamp: int
        """

        self._timestamp = timestamp
