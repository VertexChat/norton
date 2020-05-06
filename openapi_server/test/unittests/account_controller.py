import json
import uuid

import requests

url = "http://localhost:8080/api/v1"
testuser = {
    "username": f"TestUser-{str(uuid.uuid4())}",
    "password": "FooBar"
}


def test_valid_login(payload):
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", f'{url}/login', headers=headers, data=json.dumps(payload))

    assert response.status_code == 204
    assert 'Set-Cookie' in response.headers
    assert 'session_id' in response.headers['Set-Cookie']


def test_valid_registration(payload):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", f'{url}/register', headers=headers, data=json.dumps(payload))
    assert response.status_code == 201
    assert 'Location' in response.headers


def run_tests():
    test_valid_registration(testuser)
    test_valid_login(testuser)
