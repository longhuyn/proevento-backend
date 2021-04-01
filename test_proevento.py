#########################################################
#   Do 'pytest' in the server folder to run this test   #
#########################################################

import requests
import json
from notification import *
from event import *

headers = {
    'content-type': 'application/json'
}

# Test 1: trying to get an event with invalid eventId
def test_getting_invalid_eventId():
    r = requests.get('http://proevento.tk:3000/event/10000')
    assert r.status_code == 400

# Test 2: getting an event with an eventId as a character
def test_getting_invalid_eventId_with_character():
    r = requests.get('http://proevento.tk:3000/event/usc')
    assert r.status_code == 400

# Test 3: inserting a valid event
def test_creating_new_event():
    payload = {
        "userId": 9,
        "eventName": "PyTest Event",
        "description": "PyTest Description",
        "tags": [
            "tag1",
            "tag2"
        ],
        "eventImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg",
        "participants": [1, 2, 3],
        "type": 0,
        "date": "2021-03-17T19:58"
    }
    r = requests.post('http://proevento.tk:3000/event/create_event', data=json.dumps(payload), headers=headers)
    if (r.status_code != 200):
        assert r.status_code != 200
    results = json.loads(r.text)
    r = requests.get('http://proevento.tk:3000/event/' + str(results["eventId"]))
    results = json.loads(r.text)
    assert r.status_code == 200 and \
            results["userId"] == 9 and \
            results["eventName"] == "PyTest Event" and \
            results["description"] == "PyTest Description" and \
            results["participants"] == [1, 2, 3] and \
            results["type"] == "0"

#Test 4: inserting an event with invalid user id
def test_new_event_invalid_id():
    payload = {
        "userId": 999,
        "eventName": "PyTest Event 2",
        "description": "PyTest Description",
        "tags": [
            "tag1",
            "tag2"
        ],
        "eventImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg",
        "participants": [1, 2, 3],
        "type": 0,
        "date": "2021-03-17T19:58"
    }
    r = requests.post('http://proevento.tk:3000/event/create_event', data=json.dumps(payload), headers=headers)
    assert r.status_code == 500

#Test 5: inserting an event with no date
def test_new_event_no_date():
    payload = {
        "userId": 999,
        "eventName": "PyTest Event 2",
        "description": "PyTest Description",
        "tags": [
            "tag1",
            "tag2"
        ],
        "eventImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg",
        "participants": [1, 2, 3],
        "type": 0,
        "date": ""
    }
    r = requests.post('http://proevento.tk:3000/event/create_event', data=json.dumps(payload), headers=headers)
    assert r.status_code == 500

#Test 6: inserting an event with empty name and description
def test_new_event_empty_name():
    payload = {
        "userId": 1,
        "eventName": "",
        "description": "",
        "tags": [
            "tag1",
            "tag2"
        ],
        "eventImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg",
        "participants": [1, 2, 3],
        "type": 0,
        "date": "2021-03-17T19:58"
    }
    r = requests.post('http://proevento.tk:3000/event/create_event', data=json.dumps(payload), headers=headers)
    assert r.status_code == 200

# Test 7: getting all public events
def test_getting_public_events():
    r = requests.get('http://proevento.tk:3000/event/public')
    check = True
    for row in json.loads(r.text):
        if ("type" not in row or row["type"] != "0"):
            check = False
            break
    assert r.status_code == 200 and check == True

# Test 8: getting events of an invalid user
def test_getting_user_events_with_invalid_userId():
    r = requests.get('http://proevento.tk:3000/event/user/10000')
    results = json.loads(r.text)
    assert r.status_code == 200 and len(results) == 0

# Test 9: getting events of a valid user
def test_getting_user_events_with_valid_userId():
    r = requests.get('http://proevento.tk:3000/event/user/1')
    assert r.status_code == 200

# Test 10: test getting all events
def test_getting_all_events():
    r = requests.get('http://proevento.tk:3000/event/all')
    assert r.status_code == 200

# Test 11: trying to get an user with invalid userId
def test_getting_invalid_userId():
    r = requests.get('http://proevento.tk:3000/user/10000')
    assert r.status_code == 400

# Test 12: trying to create a user
def test_creating_new_user():
    payload = {
        "fullName": "PyTest PyTest",
        "username": "pytest",
        "email" : "pytest@gmail.com",
        "profileImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg"
    }
    r = requests.post('http://proevento.tk:3000/user/create_user', data=json.dumps(payload), headers=headers)
    if (r.status_code != 200):
        assert r.status_code != 200
    results = json.loads(r.text)
    r = requests.get('http://proevento.tk:3000/user/' + str(results["userId"]))
    results = json.loads(r.text)
    assert r.status_code == 200 and \
            results["fullName"] == "PyTest PyTest" and \
            results["username"] == "pytest" and \
            results["email"] == "pytest@gmail.com" and \
            results["profileImage"] == "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg"

# Test 13: trying to create an invalid user with missing email
def test_creating_invalid_user_missing_email():
    payload = {
        "fullName": "PyTester PyTesting",
        "username": "pytester",
        "profileImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg"
    }
    r = requests.post('http://proevento.tk:3000/user/create_user', data=json.dumps(payload), headers=headers)
    assert r.status_code == 500

# Test 14: trying to create an invalid user with missing username and full name
def test_creating_invalid_user_msising_name():
    payload = {
        "email" : "pytest@gmail.com",
        "profileImage": "https://images-na.ssl-images-amazon.com/images/I/614oJ8yhdKL._AC_SX466_.jpg"
    }
    r = requests.post('http://proevento.tk:3000/user/create_user', data=json.dumps(payload), headers=headers)
    assert r.status_code == 500

# Test 15: searching for an event using a key word
def test_searching_event():
    r = requests.get('http://proevento.tk:3000/search/event/public')
    assert r.status_code == 200

# Test 16: searching for a user using a key word
def test_searching_user():
    r = requests.get('http://proevento.tk:3000/search/user/Cente')
    assert r.status_code == 200

# Test 17: searching an event using a tag
def test_searching_event_tag():
    r = requests.get('http://proevento.tk:3000/search/tags/tag1')
    assert r.status_code == 200

# Test 18: getting profile of an invalid user
def test_user_profile_invalid():
    r = requests.get('http://proevento.tk:3000/profile/999')
    assert r.status_code == 400


# Test 19: adding a tag to a user profile
def test_adding_tag():
    payload = {
        "tags": ["pytest1"]
    }
    r = requests.post('http://proevento.tk:3000/profile/tag/1', data=json.dumps(payload), headers=headers)
    assert r.status_code == 200

# Test 20: getting notifications for a user
def test_sending_notification():
    r = requests.get('http://proevento.tk:3000/notification/event/1')
    assert r.status_code == 200
