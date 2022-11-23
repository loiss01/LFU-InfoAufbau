from sqlite3 import *

from os.path import abspath

database_connection = connect(abspath("twitter.db"))

with database_connection:
    database_cursor = database_connection.cursor()

    sql_statement = """SELECT user_id FROM users WHERE 2022-users.year_of_birth > 60;"""

    database_cursor.execute(sql_statement)

    for userid in database_cursor:
        print(userid[0])
        sql_statement = "DELETE FROM users WHERE user_id = " + str(userid[0])
        database_cursor.execute(sql_statement)
        sql_statement = "DELETE FROM followers where id_of_followee = "+ str(userid[0])
        database_cursor.execute(sql_statement)
        sql_statement = "DELETE FROM tweets WHERE id_of_user = "+ str(userid[0])
        database_cursor.execute(sql_statement)