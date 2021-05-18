import json
import sqlite3
from datetime import date
# from event import *
from zoomAPI import *
import ast
from datetime import datetime
from pytz import timezone


def dictFactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getUser(userId):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM User WHERE userId = ?", (userId,))
        userData = cur.fetchone()
        userData = dictFactory(cur, userData)
        return userData

def createEventNotification(userId, eventId, groupId):
    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            print(eventId)
            cur.execute("SELECT * from Event WHERE eventId = ?", (eventId,))
            con.commit()
            res = cur.fetchone()
            print(res)
            res = dictFactory(cur, res)
            print(res)
            eventName = res["eventName"]
            cur.execute("SELECT participants FROM UserGroup WHERE groupId = ?",(groupId,))
            res = cur.fetchone()
            res = dictFactory(cur, res)
            participants = ast.literal_eval(res["participants"])
            date = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
            Type = "EVENT"
            print(participants)
            for recipientId in participants:
                cur.execute("INSERT INTO Notification (recipientId, type, date, eventId, eventName, userId) VALUES (?,?,?,?,?,?)", (recipientId, Type, date, eventId, eventName, userId))
            con.commit()
            print("This thing ran all the way through")  

    except sqlite3.Error as err:
        print(str(err))

def createEvent(suggestions, groupId):
    for suggestion in suggestions:
        print(suggestion)
        userId = suggestion["userId"]
        eventName = suggestion["name"]
        description = suggestion["description"]
        date = suggestion["date"]
        eventImage = suggestion["eventImage"]
        tags = suggestion["tags"]
        categories = suggestion["categories"]
        favorites = "[]"
        recorded = suggestion["recorded"]
        participants = "[]"
        numParticipate = 1
        eventType = True
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT email from User where userId = ?", (userId,))
                email = cur.fetchone()[0]
                joinurl = create_meeting(email)
                cur.execute("INSERT INTO Event (userId, eventName, description, participants, type, date, \
                                zoomLink, favorites, eventImage, numParticipate, categories, tags, recorded) \
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                    (userId, eventName, description, participants, eventType, 
                                    date, joinurl, favorites, eventImage, numParticipate, categories, tags, recorded))
                con.commit()
                cur.execute("SELECT eventId FROM Event WHERE zoomLink = ? AND eventImage = ?",(joinurl, eventImage,))
                res = cur.fetchone()
                res = dictFactory(cur, res)
                print(res)
                eventId = res["eventId"]
                createEventNotification(userId, eventId, groupId)
        except sqlite3.Error as err:
            print(str(err))

def getGroup(groupId):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT suggestionDate FROM UserGroup WHERE groupId = ?",(groupId,))
        suggestDate = cur.fetchone()
        #suggestDate = dictFactory(cur,date)
        print(type(suggestDate))
        cur.execute("SELECT * FROM GroupSuggestion WHERE groupId = ? AND status = ?", (groupId,"PENDING",))
        rows = cur.fetchall()
        results = []
        compareDate = datetime(2025,5,3)
        try:
            compareDate = datetime.strptime(suggestDate[0], "%Y-%m-%d")
        except TypeError:
            pass

        today = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d')
        today = datetime.strptime(today, "%Y-%m-%d")
        status = "CREATED"
        status2 = "PASSED"
        print("These are the resutls")
        print(results)
        for row in rows:
            results.append(dictFactory(cur, row))
        if len(results) <=3 and len(results) > 0 and today >= compareDate:
            for suggestion in results:
                cur.execute("UPDATE GroupSuggestion SET status = ? WHERE id =?",(status, suggestion["id"],))
            con.commit()
            createEvent(results, groupId)
        elif len(results) > 0 and  today >= compareDate:
            top3Suggestions = [0,0,0]
            top3 = [0,0,0]
            for suggestion in results:
                if suggestion["voters"] == None:
                    temp = 0
                else:
                    temp = len(ast.literal_eval(suggestion["voters"]))+1
                if temp > top3[2]:
                    top3.pop(0)
                    top3.append(temp)
                    top3Suggestions.pop(0)
                    top3Suggestions.append(suggestion)
                elif temp > top3[1]:
                    nowThird = top3[1]
                    top3[1] = temp
                    top3[0] = nowThird
                    nowThird = top3Suggestions[1]
                    top3Suggestions[1] = suggestion
                    top3Suggestions[0] = nowThird
                elif temp > top3[0]:
                    top3[0] = temp
                    top3Suggestions[0] = suggestion
                else:
                    pass
            
            for suggestion in results:
                cur.execute("UPDATE GroupSuggestion SET status = ? WHERE id =?",(status2, suggestion["id"],))
            con.commit()
            for suggestion in top3Suggestions:
                cur.execute("UPDATE GroupSuggestion SET status = ? WHERE id =?",(status, suggestion["id"],))
            con.commit()
            createEvent(top3Suggestions, groupId)


        cur.execute("SELECT * FROM UserGroup WHERE groupId = ?", (groupId,))
        res = cur.fetchone()
        if (res == None):
            return {"err": "Unable to find a group with groupId " + groupId}, 400
        res = dictFactory(cur, res)
        users = []
        res["participants"] = json.loads(res["participants"])
        res["categories"] = json.loads(res["categories"])
        res["owner"] = getUser(res["ownerId"])
        for user in res["participants"]:
            users.append(getUser(user))
        res["participants"] = users
        return res