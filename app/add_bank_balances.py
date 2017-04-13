import mysql.connector
from datetime import date, datetime, timedelta
import csv

cnx = mysql.connector.connect(user='Andrew', password='Kindle01',
                              host='127.0.0.1',
                              database='kean')

cursor = cnx.cursor()

add_balances = ("INSERT INTO bank_account_balances"
                "(bank_name, account, account_balance, balance_date)"
                "VALUES(%s, %s, %s, %s)")

with open('data/account balances.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        cursor.execute(add_balances, row)

cnx.commit()

cursor.close()

cnx.close()
