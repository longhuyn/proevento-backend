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
            data = request.get_json(force=True)
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
                    return {"userId": rows["userId"]}, 200

                cur.execute("INSERT INTO User (fullName, username, email, profileImage) VALUES (?,?,?,?)",
                            (fullName, username, email, profileImage))
                con.commit()

                userId = cur.lastrowid  # return userId of the new user
                cur.execute(
                    "INSERT INTO Profile (userId, followers, following, tags) VALUES (?, '[]', '[]', '[]')", (userId,))
                name = fullName.split(" ")
                zoomAPI.add_user(name[0], name[1], email)
                return {"msg": "Sucessfully added new user to the database", "userId": userId}, 200

        except sqlite3.Error as err:
            print(str(err))
            return {"error": "Unable to add new user"}, 400