from sqlite3 import *

from prettytable import *
from os.path import abspath

database_connection = connect(abspath("twitter.db"))

with database_connection:
    database_cursor = database_connection.cursor()

    sql_statement = """SELECT users.city
FROM users
WHERE user_id IN (SELECT followers.id_of_follower
                  FROM users, followers
                  WHERE users.user_id = followers.id_of_followee AND (2022 - users.year_of_birth) >= 30)"""

    database_cursor.execute(sql_statement)
    printTable(database_cursor);