from sqlite3 import *

from prettytable import *
from os.path import abspath

database_connection = connect(abspath("twitter.db"))

with database_connection:
    database_cursor = database_connection.cursor()

    sql_statement = "SELECT gender, 2022 - max(year_of_birth) FROM users GROUP BY gender ORDER BY COUNT(gender)"

    database_cursor.execute(sql_statement)
    printTable(database_cursor);