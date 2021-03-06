from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import json
import zoomAPI
from util import *

class UserAPI(Resource):

    def get(self, userId):
        rows = {}
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from User WHERE userId = ?", (userId,))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "userId does not exist"}, 400
                rows = dictFactory(cur, rows)
                return rows, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get user with id " + userId
            return {"error": msg}, 400

    def put(self, userId):
        try:
            data = request.get_json()
            print(userId)
            name = data["fullName"]
            profileImage = data['profileImage']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                updateStr = "UPDATE User SET "
                for key, val in data.items():
                    updateStr += key + "=?, "
                updateStr = updateStr[:-2]  # remove the last comma from string
                updateStr += "WHERE userid = ?"
                temp = list(data.values())
                temp.append(userId)
                cur.execute(updateStr, tuple(temp))
                con.commit()
                return {"msg": "Successfully modified user's data"}, 200

        except sqlite3.Error as err:
            msg = "Unable to edit user's data for userId " + userId
            return {"error": msg}, 400

class UserDeleteAPI(Resource):
    def post(self, userId):
        try:
             with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM User Where userId = ?", (userId,))
                con.commit()
                cur.execute("DELETE FROM Event Where userId = ?", (userId,))
                con.commit()
                cur.execute("DELETE FROM Profile Where userId = ?", (userId,))
                con.commit()
                
                cur.execute("DELETE FROM Notification Where userId = ?", (userId,))
                con.commit()
                cur.execute("DELETE FROM UserGroup Where ownerId = ?", (userId,))
                con.commit()
                
                cur.execute("DELETE FROM Notification Where recipientId = ?", (userId,))
                con.commit()
                cur.execute("DELETE FROM ChatMessage WHERE userId = ?",(userId,))
                con.commit()
                cur.execute("DELETE FROM GroupChat WHERE userId = ?",(userId,))
                print("Made it")
                con.commit()
                cur.execute("Select userId from User")
                rows = cur.fetchall()
                for row in rows:
                    for personFollowing in row:
                        cur.execute(
                            "SELECT * from Profile WHERE userId = ?", (personFollowing,))
                        rows = cur.fetchone()
                        rows = dictFactory(cur, rows)
                        followers = json.loads(rows["followers"])
                        following = json.loads(rows["following"])
                        print(followers)
                        print(following)
                        print(type(userId))
                        print(type(followers))
                        if int(userId) in followers:
                            followers.remove(int(userId))
                            cur.execute("UPDATE Profile SET followers = ? WHERE userId = ?",
                                        (json.dumps(followers), personFollowing))
                            msg = "Sucessfully deleted from follower list"
                            print(msg)
                        if userId in following:
                            following.remove(userId)
                            cur.execute("UPDATE Profile SET following = ? WHERE userId = ?",
                                        (json.dumps(following), personFollowing))
                            msg = "Sucessfully deleted from following list"
                            print(msg)
                cur.execute("SELECT * from UserGroup")
                rows = cur.fetchall() 
               
                if(rows!= None):
                    for row in rows:               
                        data = dictFactory(cur, row)
                        print(data)
                        parts = json.loads(data["participants"])
                        print(parts)
                        if len(parts)>0:
                            try:
                                while True:
                                    parts.remove(str(userId))
                            except ValueError:
                                pass
                            cur.execute("UPDATE UserGroup SET participants = ? WHERE groupId = ?", (json.dumps(parts), data["groupId"]))
                            con.commit()
                return{"msg": "Successfully deleted user's data"},200
        except sqlite3.Error as err:
            msg = "Unable to edit user's data for userId " + userId
            return {"error": msg}, 400
            
class UserCreateAPI(Resource):

    def post(self):
        try:
            data = request.get_json()
            fullName = data['fullName']
            username = data['username']
            email = data['email']
            profileImage = data['profileImage']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from User WHERE email = ?", (email,))
                rows = cur.fetchone()
                if (rows != None):
                    rows = dictFactory(cur, rows)
                    return {"userId": rows["userId"], "first": False}, 200

                cur.execute("INSERT INTO User (fullName, username, email, profileImage) VALUES (?,?,?,?)",
                            (fullName, username, email, profileImage))
                con.commit()

                userId = cur.lastrowid  # return userId of the new user
                cur.execute(
                    "INSERT INTO Profile (userId, followers, following, tags) VALUES (?, '[]', '[]', '[]')", (userId,))
                name = fullName.split(" ")
                zoomAPI.add_user(name[0], name[1], email)
                return {"msg": "Sucessfully added new user to the database", "userId": userId, "first": True}, 200

        except sqlite3.Error as err:
            print(str(err))
            return {"error": "Unable to add new user"}, 400