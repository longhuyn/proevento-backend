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
                cur.execute("SELECT * from Profile WHERE userId = ?", (userId,))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "UserId doesn't exist"}, 400
                rows = dictFactory(cur, rows)
                rows["tags"] = json.loads(rows["tags"])
                print(rows["followers"])
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
                    print(msg)

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
                        # send notification

                        # this line causes an error so i commented it  out
                        # followerNotification(userId, followerId) 
                        msg += " and updated following list"
                    else:
                        msg = "User already exists in the following database"
                        return {"error" :msg}, 400
                    
                    cur.execute("SELECT * FROM UserChat WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)",
                                (userId, followerId, followerId, userId))
                    res = cur.fetchone()
                    if (res == None):
                        cur.execute("INSERT INTO UserChat (user1, user2) VALUES (?, ?)", (userId, followerId))    
                    
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
                if int(followerId) in followers:
    
                    followers.remove(int(followerId))
                    cur.execute("UPDATE Profile SET followers = ? WHERE userId = ?",
                                (json.dumps(followers), userId))
                    msg = "Sucessfully deleted the follower"
                    print(msg)

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
                cur.execute("UPDATE Profile SET tags = ? WHERE userId = ?", (tags, userId))
                msg = "Sucessfully added tags to the database"
                return msg, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Failed to add tags"
            return msg, 400

class ProfileBioAPI(Resource):

    def post(self, userId):
        try:
            data = request.get_json()
            bio = data['bio']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Profile SET bio = ? WHERE userId = ?", (bio, userId))
                msg = "Sucessfully added bio to the database"
                return msg, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Failed to add bio"
            return msg, 400

class ProfileBadgeAPI(Resource):

    def get(self, userId):
        rows = {}
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT badges from Profile WHERE userId = ?", (userId,))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "UserId doesn't exist"}, 400
                rows = dictFactory(cur, rows)
                if rows["badges"] != None:
                    badgeList = json.loads(rows["badges"])
                else:
                    badgeList = []
                return badgeList, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get profile with userId " + userId
            return {"error": msg}, 400

    def post(self, userId):
        try:
            data = request.get_json()
            badges = data["badges"]
            badges = json.dumps(badges)

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Profile SET badges = ? WHERE userId = ?", (badges, userId))
                msg = "Sucessfully added badges to the database"
                return msg, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Failed to add tags"
            return msg, 400