# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create a User
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
            '/api/v1/users',
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        Delete a User
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/users/{user_id}'.format(user_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user(self):
        """Test case for get_user

        Get a User
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/users/{user_id}'.format(user_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_users(self):
        """Test case for get_users

        List All users
        """
        headers = { 
            'Accept': 'application/json',
            'LoginRequired': 'special-key',
        }
        response = self.client.open(
            '/api/v1/users',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user(self):
        """Test case for update_user

        Update a User
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
            '/api/v1/users/{user_id}'.format(user_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
