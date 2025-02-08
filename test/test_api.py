import json
import pytest

# Test case for sign-up endpoint
def test_sign_up(api_client):
    # Test data
    payload = {
        "name": "testuser",
        "email": "testuser@example.com",
    }

    # Make the request
    response = api_client.post(f"{api_client.base_url}/sign-up", json=payload)

    # Assertions
    assert response.status_code == 200, "Expected status code 200"

# test login endpoint
def test_log_in(api_client):
    payload = {
        "email": "webwaymark@gmail.com",
        "password": "Asdf111$"
    }

    # successful login
    response = api_client.post(f"{api_client.base_url}/log-in", json=payload)
    assert response.status_code == 200, "Expected status code 200"

    # bad credentials
    payload = {
        "email": "webwaymark@gmail.com",
        "password": "asdf111$"
    }

    response = api_client.post(f"{api_client.base_url}/log-in", json=payload)
    error = json.loads(response.text).get('error')
    assert error == 'Bad Credentials', "Expected Bad Credentials message"


# login_required functionalit
def test_login_check(api_client):
    response = api_client.get(f"{api_client.base_url}/login-check")
    assert response.status_code == 400, "Expected status code 400"

    # Make the request with empty the token
    headers = {"x-access-token": ""}
    response = api_client.get(f"{api_client.base_url}/login-check", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # request with token
    headers = {"x-access-token": "secret"}
    response = api_client.get(f"{api_client.base_url}/login-check", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # mimic as secret and jwt token
    headers = {"x-access-token": "secret jwt"}
    response = api_client.get(f"{api_client.base_url}/login-check", headers=headers)
    assert response.status_code == 403, "Expected status code 403"