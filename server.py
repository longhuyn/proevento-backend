from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from user import *
from profile import *
from viewFollow import *
from flask_cors import CORS
from event import *
from notification import *
from search import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

# User APIS
api.add_resource(UserAPI, '/user/<userId>')
api.add_resource(UserCreateAPI, '/user/create_user')

# Profile APIS
api.add_resource(ProfileAPI, '/profile/<userId>')
api.add_resource(ProfileTagAPI, '/profile/tag/<userId>')
api.add_resource(ProfileFollowAPI, '/profile/follow/<userId>')
api.add_resource(viewFollowAPI, '/profile/viewFollow/<userId>') #might need to add true false param here
api.add_resource(checkFollowAPI, '/profile/checkFollow/<userId>')

# Event APIS
api.add_resource(GetEventAPI, '/event/<eventId>')
api.add_resource(CreateEventAPI, '/event/create_event')
api.add_resource(GetUserEventsAPI, '/event/user/<userId>')
api.add_resource(GetAllEventsAPI, '/event/all')
api.add_resource(GetPublicEventsAPI, '/event/public')

# Notification APIS
api.add_resource(EventNotificationAPI, '/notification/event/<recipientId>')

# Search APIS
api.add_resource(EventSearchAPI, '/search/event/<searchText>')
api.add_resource(UserSearchAPI, '/search/user/<searchText>')
api.add_resource(TagSearchAPI, '/search/tags/<searchText>')
api.add_resource(DateSearchAPI, '/search/date/<searchText>')
api.add_resource(SingleUserSearchAPI, '/search/single/<searchText>')
api.add_resource(SingleEventSearchAPI, '/search/single_event/<searchText>')
api.add_resource(SingleUserIdSearchAPI, '/search/singleid/<searchText>')

@app.route('/') 
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

