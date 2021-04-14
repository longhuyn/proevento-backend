import json
import sqlite3

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

def getGroup(groupId):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
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