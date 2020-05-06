# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.channel import Channel  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.message import Message  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase


class TestChannelController(BaseTestCase):
    """ChannelController integration test stubs"""

    def test_add_user_to_channel(self):
        """Test case for add_user_to_channel

        
        """
        user = {
  "id" : 0,
  "name" : "Bob"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/members'.format(channel_id=56),
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_channel(self):
        """Test case for create_channel

        Create a Channel
        """
        channel = {
  "name" : "name",
  "id" : 0,
  "type" : "TEXT"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels',
            method='POST',
            headers=headers,
            data=json.dumps(channel),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_message(self):
        """Test case for create_message

        Create a Message
        """
        message = {
  "author" : 102,
  "channel" : 110,
  "id" : 101,
  "content" : "What time is the meeting",
  "timestamp" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/messages'.format(channel_id=56),
            method='POST',
            headers=headers,
            data=json.dumps(message),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_channel(self):
        """Test case for delete_channel

        Delete a Channel
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}'.format(channel_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_message(self):
        """Test case for delete_message

        Delete a Message
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/messages/{message_id}'.format(channel_id=56, message_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_channel(self):
        """Test case for get_channel

        Get a Channel
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}'.format(channel_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_channel_members(self):
        """Test case for get_channel_members

        List All members
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/members'.format(channel_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_channels(self):
        """Test case for get_channels

        List All channels
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_message(self):
        """Test case for get_message

        Get a Message
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/messages/{message_id}'.format(channel_id=56, message_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_messages(self):
        """Test case for get_messages

        List All messages
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/messages'.format(channel_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_channel_member(self):
        """Test case for remove_channel_member

        Remove as User
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/members/{user_id}'.format(channel_id=56, user_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_channel(self):
        """Test case for update_channel

        Update a Channel
        """
        channel = {
  "name" : "name",
  "id" : 0,
  "type" : "TEXT"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}'.format(channel_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(channel),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_message(self):
        """Test case for update_message

        Update a Message
        """
        message = {
  "author" : 102,
  "channel" : 110,
  "id" : 101,
  "content" : "What time is the meeting",
  "timestamp" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/channels/{channel_id}/messages/{message_id}'.format(channel_id=56, message_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(message),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
