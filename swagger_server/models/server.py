# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Server(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, user_count: int = None, app_version: str = None):  # noqa: E501
        """Server - a model defined in Swagger

        :param user_count: The user_count of this Server.  # noqa: E501
        :type user_count: int
        :param app_version: The app_version of this Server.  # noqa: E501
        :type app_version: str
        """
        self.swagger_types = {
            'user_count': int,
            'app_version': str
        }

        self.attribute_map = {
            'user_count': 'userCount',
            'app_version': 'appVersion'
        }
        self._user_count = user_count
        self._app_version = app_version

    @classmethod
    def from_dict(cls, dikt) -> 'Server':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Server of this Server.  # noqa: E501
        :rtype: Server
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_count(self) -> int:
        """Gets the user_count of this Server.


        :return: The user_count of this Server.
        :rtype: int
        """
        return self._user_count

    @user_count.setter
    def user_count(self, user_count: int):
        """Sets the user_count of this Server.


        :param user_count: The user_count of this Server.
        :type user_count: int
        """

        self._user_count = user_count

    @property
    def app_version(self) -> str:
        """Gets the app_version of this Server.


        :return: The app_version of this Server.
        :rtype: str
        """
        return self._app_version

    @app_version.setter
    def app_version(self, app_version: str):
        """Sets the app_version of this Server.


        :param app_version: The app_version of this Server.
        :type app_version: str
        """

        self._app_version = app_version
