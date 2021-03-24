import json
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from util import *

class EventSearchAPI(Resource):

    def get(self, searchText):
    
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Event WHERE type = 0 AND eventName LIKE ?", ("%"+searchText+"%",))
                rows = cur.fetchall()
                results = []
                if (rows):
                    for row in rows:
                        results.append(getEvent(row[0]))
                return results, 200
                
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400

def getEvent(eventId):
    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from Event WHERE eventId = ?", (eventId,))
            rows = cur.fetchone()
            if (rows == None):
                return {"error": "eventId does not exist"}, 400
            rows = dictFactory(cur, rows)
            rows["tags"] = json.loads(rows["tags"])
            rows["participants"] = json.loads(rows["participants"])
            rows["favorites"] = json.loads(rows["favorites"])
            cur.execute("SELECT * FROM User WHERE userId = ?", (rows["userId"],))
            ownerData = cur.fetchone()
            ownerData = dictFactory(cur, ownerData)
            rows["owner"] = ownerData

            return rows

    except sqlite3.Error as err:
        print(str(err))
        msg = "Unable to get event with id " + eventId
        return {"error": msg}

class UserSearchAPI(Resource):

    def get(self, searchText):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM User WHERE fullName LIKE ?", ("%"+searchText+"%",))
                con.commit()
                rows = cur.fetchall()
                results = []
                if (rows):
                    for row in rows:
                        results.append(dictFactory(cur, row))
                cur.close()
                for diction in results:
                    diction["followButton"] = "follow"
                return results, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400

class TagSearchAPI(Resource):

    def get(self, searchText):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                splitText = searchText.split(',')
                results = []
                for tag in splitText:
                    cur.execute("SELECT * FROM Event WHERE type = 0 AND tags LIKE ?", ("%"+tag+"%",))
                    con.commit()
                    rows = cur.fetchall()
                    if (rows):
                        for row in rows:
                            if dictFactory(cur, row) not in results:
                                results.append(getEvent(row[0]))
                cur.close()
                return results, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400

class SingleUserSearchAPI(Resource):

    def get(self, searchText):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT userId FROM User WHERE email = ?", (searchText,))
                con.commit()
                rows = cur.fetchall()
                results = []
                if (rows):
                    for row in rows:
                        results.append(dictFactory(cur, row))
                cur.close()
                return results, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400
class SingleUserIdSearchAPI(Resource):

    def get(self, searchText):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT fullName FROM User WHERE userId = ?", (searchText,))
                con.commit()
                rows = cur.fetchall()
                results = []
                if (rows):
                    for row in rows:
                        results.append(dictFactory(cur, row))
                cur.close()
                return results, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400

class SingleEventSearchAPI(Resource):

    def get(self, searchText):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT eventId FROM Event WHERE eventName = ?", (searchText,))
                con.commit()
                rows = cur.fetchall()
                results = []
                if (rows):
                    for row in rows:
                        results.append(dictFactory(cur, row))
                cur.close()
                return results[-1], 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400

class DateSearchAPI(Resource):

    def get(self, searchText):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT eventId FROM Event WHERE date LIKE ?", ("%"+searchText+"%",))
                con.commit()
                rows = cur.fetchall()
                print(rows)
                results = []
                if (rows):
                    for row in rows:
                        if dictFactory(cur, row) not in results:
                            results.append(getEvent(row[0]))
                cur.close()
                return results, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to perform the search"
            return {"error": msg}, 400

