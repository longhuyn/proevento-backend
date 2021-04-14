from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import json
from util import *

class GetAllCategories(Resource):

    def get(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Category ORDER BY name ASC")
                rows = cur.fetchall()
                res = []
                for row in rows:
                    res.append(dictFactory(cur, row))
                return res, 200

        except sqlite3.Error as err:
            print(str(err))
            msg = "Unable to get all categories"
            return {"error": msg}, 400