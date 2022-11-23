from sqlite3 import *

from prettytable import *
from os.path import abspath

database_connection = connect(abspath("twitter.db"))

with database_connection:
    database_cursor = database_connection.cursor()

    sql_statement = "SELECT last_name, first_name, year_of_birth FROM users ORDER BY year_of_birth;"

    database_cursor.execute(sql_statement)
    printTable(database_cursor); 