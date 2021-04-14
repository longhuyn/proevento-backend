from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import json
from chat import *
from util import *

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

                cur.execute("INSERT INTO UserGroup (ownerId, name, description, categories, logo, participants) \
                            VALUES (?, ?, ?, ?, ?, ?)", 
                            (userId, name, description, categories, logo, json.dumps(partIds)))
                con.commit()
                groupId = cur.lastrowid

                temp = con.cursor()
                temp.execute("INSERT INTO GroupChat (groupId, userId) VALUES (?, ?)", (groupId, userId))
                for row in partIds:
                    temp.execute("INSERT INTO GroupChat (groupId, userId) VALUES (?, ?)", (groupId, row))

                # TODO: send notifications to participants here, the userIds are in partsId

                return {"msg": "Successfully created a new group", "groupId": groupId}, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to create a new group"
            return {"error": msg}, 400