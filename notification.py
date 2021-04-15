from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sqlite3
import json
from util import *
from datetime import date, datetime
import event
import requests
from pytz import timezone

class getNotificationsAPI(Resource):
	def get(self, recipientId):
		try:
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM Notification WHERE recipientId = ? ORDER BY date DESC", (recipientId,))
				rows = cur.fetchall()
				results = []
				for row in rows:
					results.append(dictFactory(cur, row))
				cur.close()
				return results, 200
		except sqlite3.Error as err:
			print(str(err))
			return {"error": "Unable to get event notifications"}, 400


class FollowNotificationAPI(Resource):

	def post(self, userId, recipientId):
		try:
			date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
			Type = "FOLLOW"
			# date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
			print(date)
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM User WHERE userId = ?", (userId,))
				user = cur.fetchone()
				user = dictFactory(cur, user)
				cur.execute("INSERT INTO Notification (recipientId, type, date, userId, userName) \
							VALUES (?,?,?,?,?)", (recipientId, Type, date, userId, user["fullName"]))
				con.commit()
				cur.close()
				return {"msg": "Successfully created a follow notification"}, 200

		except sqlite3.Error as err:
			print(str(err))
			return {"error": "Unable to create follow notification"}, 400

class EventNotificationAPI(Resource):

	def post(self, recipientId):
		try:
			data = request.get_json()
			eventId = data['eventId']
			userId = data['userId']
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * from Event WHERE eventId = ?", (eventId,))
				res = cur.fetchone()
				res = dictFactory(cur, res)
				eventName = res["eventName"]
				createEventNotification(recipientId, eventId, eventName, userId)
				# event = Event(userId, eventId, email, description)
				# joinurl = event.get_joinurl()
				# cur.execute("INSERT INTO EventNotification (recipientId, eventId, date, joinurl, description) VALUES (?,?,?,?,?)", (recipientId, eventId, date, joinurl, description))
				# con.commit()
				cur.close()
		except sqlite3.Error as err:
			print(str(err))
			msg = "Unable to create event"
			return msg, 400

def createEventNotification(recipientId, eventId, eventName, userId):
	date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
	Type = "EVENT"
	# date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	# CURRENT ERROR: table Notification has no column named eventName
	print(date)
	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("INSERT INTO Notification (recipientId, type, date, eventId, eventName, userId) VALUES (?,?,?,?,?,?)", (recipientId, Type, date, eventId, eventName, userId))
		con.commit()
		cur.execute("SELECT * FROM Event WHERE eventId = ?", (eventId,))
		row = cur.fetchone()
		row = dictFactory(cur, row)
		participants = json.loads(row["participants"])
		participants.append(recipientId)
		cur.execute("UPDATE Event SET participants = ? WHERE eventId = ?", (json.dumps(participants), eventId))
		cur.close()
		
class DeleteRequestNotificationAPI(Resource):
	def post(self, notiId):
		try:
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("DELETE FROM Notification WHERE notificationId = ?", (notiId,))
				con.commit()
				return {"Success": "Deleted Notifcation"}, 200
		except sqlite3.Error as err:
			msg = "Error in deleting NOtification"
			return {"error": msg}, 400

class CancelNotificationAPI(Resource):
	def post(self, eventId):
		try:
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM Event WHERE eventId = ?", (eventId,))
				rows = cur.fetchone()
				eventName = rows["eventName"]
				if (rows == None):
					return {"error": "eventId doesn't exist"}, 400
				else:
					cur.execute("SELECT * FROM EVENT WHERE eventId = ?", (eventId,))
					res = cur.fetchone()
					res = dictFactory(cur, res)
					participants = json.loads(res["participants"])
					for user in participants:
						cancelNotification(user, eventName)
					cur.execute("DELETE FROM Event WHERE eventId = ?", (eventId,))

		except sqlite3.Error as err:
			print(str(err))
			msg = "Error in deleting event"
			return {"error": msg}, 400

	def cancelNotification(recipient, eventName):
	    date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
	    Type = "CANCEL"
	    # date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	    print(date)
	    with sqlite3.connect("database.db") as con:
		    cur = con.cursor()
		    cur.execute("INSERT INTO Notification (recipientId, type, date, eventName) VALUES (?,?,?,?)", (recipientId, Type, date, eventName))
		    con.commit()
		    cur.close()