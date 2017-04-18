
'''
This function reads a csv file from the data directory, extracts relevant
   pricing info and loads it into KEAN lmp table

'''

import csv
import mysql.connector
from datetime import date, datetime, timedelta


def read_lmp_csv_rt():

    reportdata = []
    dst_spring = ['20080309', '20090308', '20100314', '20110313', '20120311', '20130310', '20140309', '20150308', '20160313', '20170312']

    with open('data/pjm-rt.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            reportdata.append(row)


    pnode_prices = []



    for index, pnode in enumerate(reportdata[8:]):

        if pnode[0] == "End of Real Time LMP Data":
            break

        for hour in range(1,25):

            valuation_date = str(pnode[0][:8])
            #print(valuation_date)

            hourly_prices = []

            hourly_prices.append(pnode[0])
            hourly_prices.append("Real Time")
            hourly_prices.append(pnode[1])

            hour_ending = "0" + str(hour) + "00"
            hourly_prices.append(hour_ending[-4:])

            if valuation_date in dst_spring and hour_ending[-4:] == '0300':
                hourly_prices.append(0.0)
                hourly_prices.append(0.0)
                hourly_prices.append(0.0)
            else:
                hourly_prices.append(pnode[7+(hour-1)*3])
                hourly_prices.append(pnode[8+(hour-1)*3])

                if pnode[9+(hour-1)*3][-1:][-2:] == '\n\r':
                    hourly_prices.append(pnode[9+(hour-1)*3][:-2])
                elif pnode[9+(hour-1)*3][-1:][-1:] == '\n':
                    if pnode[9+(hour-1)*3][-1:][-2:] == '\r\n':
                        hourly_prices.append(pnode[9+(hour-1)*3][:-2])
                    else:
                        hourly_prices.append(pnode[9+(hour-1)*3][:-1])
                else:
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
    lightstone_pnodes = ['32418417', '32419363', '32419351', '32418701', '34497127', '40243805', '40243919', '71856731', '71856741']


    for entry in pnode_prices:
        if entry[2] in lightstone_pnodes:
            cursor.execute(add_prices, entry)
            cnx.commit()
#            print(entry)                   # use to debug



    cursor.close()

    cnx.close()


