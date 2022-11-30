from sqlite3 import *

from prettytable import printTable
from os.path import abspath

database_connection = connect(abspath("twitter.db"))

with database_connection:
    database_cursor = database_connection.cursor()

    sql_statement = """create table IF NOT EXISTS likes 
            (
                like_id  INTEGER
                    constraint PRIMERY_KEY
                        primary key autoincrement,
                user_l_id  INTEGER not null
                    constraint likes_users_null_fk
                        references users,
                tweet_id INTEGER not null
                    constraint likes_tweets_null_fk
                        references tweets
            );
            """

    database_cursor.execute(sql_statement)

    sql_statement = "INSERT INTO likes(user_l_id, tweet_id) VALUES (1,3), (4,5), (1,3),(3,4),(3,1)"

    database_cursor.execute(sql_statement)

    sql_statement = """SELECT *
FROM users
INNER JOIN likes l on users.user_id = l.user_l_id"""
    database_cursor.execute(sql_statement)

    printTable(database_cursor)