from datetime import datetime
from zoomAPI import *
import json
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from util import *
from event import *
from notification import *
import requests
import pytz

class Event:
    """Event isnt sending the notification that has to be done separately"""
    """Event will just retrieve the zoom link and they have to have confirmed the email beforehand"""
    """Event cannot do a look up of current particpants because it costs $$$ irl"""

    def __init__(self, userID, eventID, email, description):
        self.userID = userID
        self.eventID = eventID
        self.description = description
        self.date = datetime.utcnow()
        self.email = email
        
        
    def get_joinurl(self):
       return create_meeting(get_zoom_id(self.email))

class GetEventAPI(Resource):

    def get(self, eventId):
        result = getEvent(eventId)
        print(result)
        if "error" in result:
            msg = "Unable to get event with id " + eventId
            return {"error": msg}, 400
        else:
            return result, 200
            

def getEvent(eventId):
    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from Event WHERE eventId = ?", (eventId,))
            rows = cur.fetchone()
            if (rows == None):
                return {"error": "eventId does not exist"}
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

class CreateEventAPI(Resource):
    def post(self):
        try:
            data = request.get_json()

            userId = data['userId']
            eventName = data['eventName']
            description = data['description']
            tags = json.dumps(data['tags'])
            eventImage = data['eventImage']
            participants = json.dumps(data['participants'])
            favorites = "[]"
            eventType = data["type"]
            date = data['date']
            # date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT email from User where userId = ?", (userId,))
                email = cur.fetchone()[0]
                joinurl = create_meeting(email)
                cur.execute("INSERT INTO Event (userId, eventName, description, tags, participants, type, date, zoomLink, favorites, eventImage, numParticipate) \
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                (userId, eventName, description, tags, participants, eventType, date, joinurl, favorites, eventImage, 0))
                con.commit()
                eventId = cur.lastrowid
                cur.close() 
                return {"msg": "Successfully created new event", "eventId": eventId}, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to create event"
            return {"error": msg}, 400

class GetUserEventsAPI(Resource):
    def get(self, userId):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT eventId FROM Event WHERE userId = ? ORDER BY date", (userId,))
                rows = cur.fetchall()
                results = []
                for row in rows:
                    results.append(getEvent(row[0]))
                return results, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to create event"
            return {"error": msg}, 400

class GetAllEventsAPI(Resource):
    def get(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Event ORDER BY date")
                rows = cur.fetchall()
                results = []
                for row in rows:
                    results.append(getEvent(row[0]))
                return results, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to create event"
            return {"error": msg}, 400

class GetPublicEventsAPI(Resource):
    def get(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Event WHERE type = 0 ORDER BY date")
                rows = cur.fetchall()
                results = []
                for row in rows:
                    results.append(getEvent(row[0]))
                return results, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to create event"
            return {"error": msg}, 400
                

class AddParticipantAPI(Resource):
    def post(self, eventId, userId):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Event WHERE eventId = ?", (eventId,))
                rows = cur.fetchone()
                oldParticipants = json.loads(rows["participants"])
                oldParticipants.append(userId)
                oldNumParticipate = rows["numParticipate"]
                cur.execute("UPDATE Event SET participants = ? WHERE eventId = ?", (json.dumps(oldParticipants), eventId))
                cur.execute("UPDATE Event SET numParticipate = ? WHERE eventId = ?", (oldNumParticipate + 1, eventId))   
                cur.close() 
                return {"msg": "Successfully added participant"}, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Server Error"
            return {"error": msg}, 400

class TopTenAPI(Resource):
    def get(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Event ORDER BY numParticipate DESC")
                rows = cur.fetchall()
                results = []
                for x in range(10):
                    results.append(getEvent(row[0]))
                return results, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Server Error"
            return {"error": msg}, 400

class EventReviewAPI(Resource):
    def get(self, eventId):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from Event WHERE eventId = ?", (eventId,))
                rows = cur.fetchone()
                if (rows == None):
                    return {"error": "eventId does not exist"}
                rows = dictFactory(cur, rows)
                
                
                #results = []
                if rows["reviews"] != None:
                    reviewList = json.loads(rows["reviews"]) #not working json object must be a str to use loads
                else:
                    reviewList = []
                return reviewList, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get event with id " + eventId
            return {"error": msg}

    def post(self, eventId):
        try:
            data = request.get_json()
            reviews = data['reviews']
            reviews = json.dumps(reviews)

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Event SET reviews = ? WHERE eventId = ?", (reviews, eventId))
                msg = "Successfully added reviews"
                return msg, 200
        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to add review"
            return {"error": msg}, 400