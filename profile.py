import json
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from util import *

class ProfileAPI(Resource):

    def get(self, userId):
        rows = {}
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from Profile WHERE userId = ?", (userId))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "UserId doesn't exist"}, 400
                rows = dictFactory(cur, rows)
                rows["tags"] = json.loads(rows["tags"])
                rows["followers"] = json.loads(rows["followers"])
                rows["following"] = json.loads(rows["following"])
                return rows, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get profile with userId " + userId
            return {"error": msg}, 400


class ProfileFollowAPI(Resource):

    def post(self, userId):
        try:
            data = request.get_json()
            followerId = data['followerId']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "SELECT * from Profile WHERE userId = ?", (userId,))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "UserId doesn't exist"}, 400
                rows = dictFactory(cur, rows)

                followers = json.loads(rows["followers"])
                if followerId not in followers:
                    followers.append(followerId)
                    cur.execute("UPDATE Profile SET followers = ? WHERE userId = ?",
                                (json.dumps(followers), userId))
                    msg = "Sucessfully added a new follower"

                    cur = con.cursor()
                    cur.execute("SELECT * from Profile WHERE userId = ?", (followerId,))
                    rows = cur.fetchone()
                    if (rows == None):
                        return {"error": "UserId doesn't exist"}, 400
                    rows = dictFactory(cur, rows)
                    following = json.loads(rows["following"])
            
                    if userId not in following:
                        following.append(userId)
                        cur.execute("UPDATE Profile SET following = ? WHERE userId = ?",
                                (json.dumps(following), followerId))
                        msg += " and updated following list"
                    else:
                        msg = "User already exists in the following database"
                        return {"error" :msg}, 400
                        
                    return {"msg" :msg}, 200

                else:
                    msg = "Follower already exists in the database"
                    return {"error" :msg}, 400

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to add new follower"
            return msg, 400

    def put(self, userId):
        try:
            data = request.get_json(force=True)
            followerId = data['followerId']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "SELECT * from Profile WHERE userId = ?", (userId,))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "UserId doesn't exist"}, 400
                rows = dictFactory(cur, rows)

                if rows["followers"] != None:
                    followers = json.loads(rows["followers"])
                else:
                    followers = [] 

                if followerId in followers:
                    followers.remove(followerId)
                    cur.execute("UPDATE Profile SET followers = ? WHERE userId = ?",
                                (json.dumps(followers), userId))
                    msg = "Sucessfully deleted the follower"

                    cur.execute("SELECT * from Profile WHERE userId = ?", (followerId,))
                    rows = cur.fetchone()
                    if (rows == None):
                        return {"error": "UserId doesn't exist"}, 400
                    rows = dictFactory(cur, rows)
                    if rows["following"] != None:
                        following = json.loads(rows["following"])
                    else:
                        following = []
                    if userId in following:
                        following.remove(userId)
                        cur.execute("UPDATE Profile SET following = ? WHERE userId = ?",
                                (json.dumps(following), followerId))
                        msg += " and updated following list"
                   

                    return msg, 200
                else:
                    msg = "Follower does not exist in the database!!"
                    return msg, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to delete a follower"
            return msg, 400


class ProfileTagAPI(Resource):

    def post(self, userId):
        try:
            data = request.get_json(force=True)
            tags = data['tags']
            tags = json.dumps(tags)

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Profile SET tags = ?", (tags,))
                msg = "Sucessfully added tags to the database"
                return msg, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Failed to add tags"
            return msg, 400
