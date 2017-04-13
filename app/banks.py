import mysql.connector
from datetime import date, datetime, timedelta
import csv

cnx = mysql.connector.connect(user='Andrew', password='Kindle01',
                              host='127.0.0.1',
                              database='kean')

cursor = cnx.cursor()

add_account = ("INSERT INTO banks"
                "(bank_name, account, account_name)"
                "VALUES(%s, %s, %s)")

with open('data/baml accounts - 170410a.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        cursor.execute(add_account, row)
        #print(row)

cnx.commit()

cursor.close()

cnx.close()
