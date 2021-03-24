import requests
import json
"""JWT authorization tokens will need to make a new one every week"""

headers = {
	'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IlRYaHlmbTVxUjhpM0VNblo4RVFVb0EiLCJleHAiOjE2MTY4OTc3MTcsImlhdCI6MTYxNjI5MjkxN30.tCWk0AUpqU5DcZKBwqcH2KzPSKc8ACEohFzaID2ERII",
	'content-type': "application/json"
}

def add_user(first_name, last_name, email):
	"""This function adds the user to our zoom account upon initial sign up"""
	"""We will be using their inputted information to create their account"""
	"""This will return their zoomID to be stored in their profile"""
	request_body = {
        "action": "create",
        "user_info": {
            "email": email,
            "type": 1,
            "first_name": first_name,
            "last_name": last_name
        }
    }
	r = requests.post("https://api.zoom.us/v2/users", data = json.dumps(request_body), headers = headers)
	return 0

def get_zoom_id(email):
	r = requests.get("https://api.zoom.us/v2/users", headers = headers)
	information = json.loads(r.text)
	for dict in information["users"]:
		if dict["email"] == email:
			return(dict["id"])

def create_meeting(userID = "me"):
	"""This function is used to create  meetings
	The created meetings will be stored in the database
	Each time a meeting is created the URL to join it will be returned"""
	"""For use with private meetings simply do not add the joinable link to the event Feed instead attach it to the Notifications object"""
	"""For use with public meetings just add the returned link to the event Feed"""
	request_body = {
        "topic": "string",
        "type": "1",
        "settings": {
            "host_video": "true",
            "participant_video": "false",
            "registrants_email_notification": "false"
        }
    }
	r = requests.post("https://api.zoom.us/v2/users/" + str(userID) + "/meetings",data = json.dumps(request_body), headers = headers)
	information = json.loads(r.text)
	print(information)
	return information["join_url"]
