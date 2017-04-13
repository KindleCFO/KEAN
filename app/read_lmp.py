import csv
import mysql.connector
from datetime import date, datetime, timedelta

reportdata = []

with open('data/pjm-da.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')

    for row in reader:
        reportdata.append(row)


pnode_prices = []



for index, pnode in enumerate(reportdata[8:]):

    if pnode[0] == "End of Day Ahead LMP Data":
        break

    for hour in range(1,25):

        hourly_prices = []

        hourly_prices.append(pnode[0])
        hourly_prices.append("Day Ahead")
        hourly_prices.append(pnode[1])

        hour_ending = "0" + str(hour) + "00"
        hourly_prices.append(hour_ending[-4:])

        hourly_prices.append(pnode[7+(hour-1)*3])
        hourly_prices.append(pnode[8+(hour-1)*3])
        hourly_prices.append(pnode[9+(hour-1)*3])

        pnode_prices.append(hourly_prices)

#x = 235
#print(pnode_prices[x][0], pnode_prices[x][1], pnode_prices[x][2], pnode_prices[x][3], pnode_prices[x][4], pnode_prices[x][5])

cnx = mysql.connector.connect(user='Andrew', password='Kindle01',
                              host='127.0.0.1',
                              database='kean')

cursor = cnx.cursor()

add_prices = ("INSERT INTO lmp"
                "(valuation_date, dart, pnode_id, hour_ending, total_lmp, congestion_price, marginal_loss_price)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s)")


''' We only care about certain LMP locations (pnodes)
    - Gavin:        pnode = 40243805; pnode = 40243807  *appears we only grab 40243805
    - PSEGGLOB      pnode = 71856747 *22KV, not 18KV
    - LawrencC2     pnode = 71856731, 33, 37, 39, 29, 35
    - Adkins        pnode = 40243919, 21, 23, 25, 27, 29
    - AEP Hub       pnode = 34497127
'''
lightstone_pnodes = ['40243805', '71856747', '71856731', '40243919', '34497127']


for row in pnode_prices:
    if row[2] in lightstone_pnodes:
        cursor.execute(add_prices, row)


cnx.commit()

cursor.close()

cnx.close()
