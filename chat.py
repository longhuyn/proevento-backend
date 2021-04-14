import json
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from util import *
from user_group import *

class GetUserChatRoom(Resource):

    def get(self, userId):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM UserChat WHERE user1 = ? OR user2 = ?", (userId, userId))
                rows = cur.fetchall()
                res = []
                for row in rows:
                    userChatId = row[2] if (int(row[1]) == int(userId)) else row[1]
                    res.append({"roomId": row[0], "chatUser": getUser(userChatId)})

                return res, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to load user chat rooms"
            return {"error": msg}, 400

class GetGroupChatRoom(Resource):

    def get(self, userId):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM GroupChat WHERE userId = ?", (userId, ))
                rows = cur.fetchall()
                res = []
                for row in rows:
                    row = dictFactory(cur, row)
                    data = getGroup(row["groupId"])
                    data["roomId"] = row["roomId"]
                    res.append(data)
                return res, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to load user chat rooms"
            return {"error": msg}, 400


class GetChatMessages(Resource):

    def get(self, chatType, roomId):
        try:
            # data = request.get_json()
            # roomId = data["roomId"]

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM ChatMessage WHERE chatType = ? AND roomId = ? ORDER BY date ASC", (chatType, roomId))
                rows = cur.fetchall()
                res = []
                for row in rows:
                    row = dictFactory(cur, row)
                    row["chatUser"] = getUser(row["userId"])
                    res.append(row)

                return res, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to load user chat rooms"
            return {"error": msg}, 400
