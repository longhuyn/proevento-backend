from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sqlite3
import json
from util import *
from datetime import date, datetime
import event
import requests
from pytz import timezone

class followNotificationAPI(Resource):
    # def get(self, userId):
    #     try:

	def post(self, userId):
		
		try:
			data = request.get_json()
			recipientId = data['recipientId']
			status = data['status']
			date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
			# date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
			output = str(recipientId, " has followed you")
			
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO FollowNotification (recipientId, status, date, output) VALUES (?,?,?,?)", (recipientId, status, date, output))
				con.commit()
				cur.close() 
		except sqlite3.Error as err:
			print(str(err))
			msg = "Unable to create event"
			return msg, 400

class EventNotificationAPI(Resource):

	def get(self, recipientId):
		try:
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM EventNotification WHERE recipientId = ?", (recipientId,))
				rows = cur.fetchall()
				results = []
				for row in rows:
					results.append(dictFactory(cur, row))
				cur.close()
				return results, 200
		except sqlite3.Error as err:
			print(str(err))
			return {"error": "Unable to get event notifications"}, 400

	def post(self, recipientId):
		
		try:
			data = request.get_json()
			description = " has invited you to join this event. Please click on the event name to see more details"
			eventId = data['eventId']
			eventName = data['eventName']
			userId = data['userId']
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * from Event WHERE eventId = ?", (eventId,))
				res = cur.fetchone()
				res = dictFactory(cur, res)
				createEventNotification(recipientId, eventId, res["zoomLink"], description, eventName, userId)
				# event = Event(userId, eventId, email, description)
				# joinurl = event.get_joinurl()
				# cur.execute("INSERT INTO EventNotification (recipientId, eventId, date, joinurl, description) VALUES (?,?,?,?,?)", (recipientId, eventId, date, joinurl, description))
				# con.commit()
				cur.close()
		except sqlite3.Error as err:
			print(str(err))
			msg = "Unable to create event"
			return msg, 400

def createEventNotification(recipientId, eventId, joinurl, description, eventName, userId):
	date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
	# date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	print(date)
	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("INSERT INTO EventNotification (recipientId, eventId, date, joinurl, description, eventName, userId) VALUES (?,?,?,?,?,?,?)", (recipientId, eventId, date, joinurl, description, eventName, userId))
		con.commit()
		cur.close()