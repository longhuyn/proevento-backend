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
from chat import *
from flask_socketio import join_room, leave_room, SocketIO, send, emit

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# User APIS
api.add_resource(UserAPI, '/user/<userId>')
api.add_resource(UserDeleteAPI, '/user/delete_user/<userId>')
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
api.add_resource(AddParticipantAPI, '/event/<eventId>/<userId>')
api.add_resource(TopTenAPI, '/event/topten')

# Notification APIS
api.add_resource(getNotificationsAPI, '/notification/<recipientId>')
api.add_resource(FollowNotificationAPI, '/notification/follow/<userId>/<recipientId>')
api.add_resource(EventNotificationAPI, '/notification/event/<recipientId>')
api.add_resource(CancelNotificationAPI, '/notification/cancel/<eventId>')


# Search APIS
api.add_resource(EventSearchAPI, '/search/event/<searchText>')
api.add_resource(UserSearchAPI, '/search/user/<searchText>')
api.add_resource(TagSearchAPI, '/search/tags/<searchText>')
api.add_resource(DateSearchAPI, '/search/date/<searchText>')
api.add_resource(SingleUserSearchAPI, '/search/single/<searchText>')
api.add_resource(SingleEventSearchAPI, '/search/single_event/<searchText>')
api.add_resource(SingleUserIdSearchAPI, '/search/singleid/<searchText>')

# Chat APIS
api.add_resource(GetUserChatRoom, '/chat/user_chat/<userId>')
api.add_resource(GetChatMessages, '/chat/chat_messages/<chatType>/<roomId>')

# Socketio to handle live chat 
@socketio.on('send_message')
def handle_message(data):
    userId = data['userId']
    message = data['message']
    roomId = data['roomId']
    chatType = data['chatType']

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO ChatMessage (userId, roomId, message, chatType) VALUES (?, ?, ?, ?)", (userId, roomId, message, chatType))
        messageId = cur.lastrowid
        data["messageId"] = messageId
        room = str(roomId) + "_" + str(chatType)
        data["chatUser"] = getUser(userId)
        emit('get_message', data, room = room)

@socketio.on('join')
def on_join(data):
    roomId = data['roomId']
    chatType = data['chatType']
    room = str(roomId) + "_" + str(chatType)
    join_room(room)
    # send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    roomId = data['roomId']
    chatType = data['chatType']
    leave_room(str(roomId) + "_" + str(chatType))
    # send(username + ' has left the room.', to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)
    # app.run(debug=True, host='0.0.0.0', port=3000)
