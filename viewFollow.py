from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import json
from util import *

class checkFollowAPI(Resource):
    def post(self, userId):
        print(request.get_json())
        data = request.get_json()
        print(data)
        idToCheck = data["idToCheck"]
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                        "SELECT followers from Profile WHERE userId = ?", (idToCheck,))
                con.commit()
                rows = cur.fetchall()
                results = []
                cur.close()
                if (rows):
                    for row in rows:
                        results.append(dictFactory(cur, row))
           
                if (rows == None):
                    return "userId doesn't exist", 400
                
                for user in results:
                    print(user["followers"])
                    if userId in user["followers"]:
                        return "true", 200
                return "false", 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get user with id " + userId
            return msg, 400  

class viewFollowAPI(Resource):
    # retrive followers/following list
    # userId is filled based on which profile page you are currently on
    def get(self, userId):
        rows = {}
        data = request.get_json(force=True)
        viewFollowers = data['viewFollowers']

        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                if viewFollowers == True:
                    cur.execute(
                        "SELECT followers from Profile WHERE userId = ?", (userId,))
                    rows = cur.fetchone()
                    if (rows == None):
                        return "userId doesn't exist", 400
                    rows = dictFactory(cur, rows)
                    return rows, 200
                else:  # get following list
                    cur.execute(
                        "SELECT following from Profile WHERE userId = ?", (userId,))
                    rows = cur.fetchone()
                    if (rows == None):
                        return "userId doesn't exist", 400
                    rows = dictFactory(cur, rows)
                    return rows, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get user with id " + userId
            return msg, 400
