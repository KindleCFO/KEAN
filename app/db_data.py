from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'kean'

TABLES = {}

TABLES['prices'] = (
    "CREATE TABLE `prices`  ("
    "   `recID` int(11) NOT NULL AUTO_INCREMENT,"
    "   `valuation_date` date NOT NULL,"
    "   `instrument_id` varchar(15) NOT NULL,"
    "   `period` date NOT NULL,"
    "   `price` float(8,4) NOT NULL,"
    "   PRIMARY KEY(`recID`)"
    ")  ENGINE=InnoDB")

#KE uses Andrew, home uses andrew  different passwords as well
cnx = mysql.connector.connect(user='Andrew', password='Kindle01')
cursor = cnx.cursor()



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


for name, ddl in TABLES.items():

    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
