from platform_in import app as flask_app
import pytest
import json

@pytest.fixture(scope='module')
def test_client():
    #flask_app = create_app('flask_test.cfg')
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()

def test_create_user_success(test_client):
    """
    GIVEN flask app
    WHEN POST request is sent to '/registration' with valid input
    THEN check the response is 200
    """
    request_body = {
        "username":"hello",
        "email":"hello",
        "password":"hello"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = test_client.post('/registration', data=json.dumps(request_body),headers = headers)
    assert response.status_code == 200