from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import json
from chat import *
from util import *
from datetime import date, datetime
from pytz import timezone

class GetGroupAPI(Resource):

    def get(self, groupId):
        try:
            res = getGroup(groupId)
            return res, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get the group with id " + groupId
            return {"error": msg}, 400

class GetAllGroupsAPI(Resource):
    def get(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM UserGroup ORDER BY groupId")
                rows = cur.fetchall()
                results = []
                for row in rows:
                    results.append(getGroup(row[0]))
                return results, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get groups"
            return {"error": msg}, 400

class CreateGroupAPI(Resource):

    def post(self, userId):
        try:
            data = data = request.get_json()
            name = data["name"]
            description = data["description"]
            categories = json.dumps(data["categories"])
            logo = data["logo"]
            partIds = []
            participants = data["participants"]

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()

                for row in participants:
                    cur.execute("SELECT * FROM User WHERE email = ?", (row,))
                    res = cur.fetchone()
                    if (res != None):
                        res = dictFactory(cur, res)
                        partIds.append(res["userId"])

                emptyArr = []
                cur.execute("INSERT INTO UserGroup (ownerId, name, description, categories, logo, participants) \
                            VALUES (?, ?, ?, ?, ?, ?)", 
                            (userId, name, description, categories, logo, json.dumps(emptyArr)))
                con.commit()
                groupId = cur.lastrowid

                cur.execute("INSERT INTO GroupChat (groupId, userId) VALUES (?, ?)", (groupId, userId))
                con.commit()

                currentDate = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
                typeOf = "JoinGroupRequest"
                user = getUser(userId)
                for row in partIds:
                    cur.execute("INSERT INTO Notification (recipientId, date, type, groupId, userId, userName, groupName) \
                                VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                (row, currentDate, typeOf, groupId, userId, user["fullName"], name))

                return {"msg": "Successfully created a new group", "groupId": groupId}, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to create a new group"
            return {"error": msg}, 400

class AddUserToGroupAPI(Resource):
    def post (self, userId):
        try:
            data = request.get_json()
            groupId = data["groupId"]
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from UserGroup WHERE groupId = ?", (groupId,))
                rows = cur.fetchone()                
                rows = dictFactory(cur, rows)
                parts = json.loads(rows["participants"])
                parts.append(userId)
                # cur.execute("SELECT participants FROM UserGroup WHERE groupId = ?", (name,))
                # parts = cur.fetchone()
                # parts.append(userId)
                cur.execute("UPDATE UserGroup SET participants = ? WHERE groupId = ?", (json.dumps(parts), groupId))
                addUserToGroupChat(con, groupId, userId)
                return {"msg": "Successfully added user to group"}, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to add user to group"
            return {"error": msg}, 400

class SendRequestUserJoinGroupAPI(Resource):
    def post(self, recipientId):
        try:
            data = request.get_json()
            groupId = data["groupId"]
            userId = data["userId"]
            currentDate = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
            user = getUser(userId)
            #currentDate =str(date.today())
            Type = "JoinGroupRequest"
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM UserGroup WHERE groupId = ?", (groupId,))
                groupData = cur.fetchone()
                groupData = dictFactory(cur, groupData)
                cur.execute("INSERT INTO Notification (recipientId, date, type, groupId, userId, userName, groupName) \
                            VALUES (?, ?, ?, ?, ?, ?, ?)", 
                            (recipientId, currentDate, Type, groupId, userId, user["fullName"], groupData["name"]))
                cur.close()
                return {"msg": "Successfully requested user to group"}, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to add user to group"
            return {"error": msg}, 400
            
class SendRequestOwnerGroupAPI(Resource):
    def post(self):
        try:
            data = request.get_json()
            groupId = data["groupId"]
            userId = data["userId"]
            currentDate = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
            Type = "RequestGroupOwner"
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT ownerId FROM UserGroup WHERE groupId = ?", (groupId,))
                rows = cur.fetchone()                
                rows = dictFactory(cur, rows)
                recipientId = rows["ownerId"]
                recipient = getUser(userId)

                cur.execute("SELECT * FROM UserGroup WHERE groupId = ?", (groupId,))
                groupData = cur.fetchone()
                groupData = dictFactory(cur, groupData)
                cur.execute("INSERT INTO Notification (recipientId, date, type, groupId, userId, userName, groupName) \
                            VALUES (?,?,?,?,?,?,?)", 
                            (recipientId, currentDate, Type, groupId, userId, recipient["fullName"], groupData["name"]))
                
                cur.close()
                return {"msg": "Successfully requested owner to join group"}, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to add user to group"
            return {"error": msg}, 400

def addUserToGroupChat(con, groupId, userId):
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO GroupChat (groupId, userId) VALUES (?, ?)", (groupId, userId))
        con.commit()
    except sqlite3.Error as err:
        print(str(err))
        msg = "Unable to add user to group chat"