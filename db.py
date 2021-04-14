import sqlite3
import os

try:
    os.system("rm database.db")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql_file = open("schema.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

except sqlite3.Error as err:
    print(str(err))

conn.close()
