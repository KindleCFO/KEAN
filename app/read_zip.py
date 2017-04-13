'''
Older prices use different pnodes, formats, and detail
    - change pnode_id at some point
    - report congestion_price and marginal_loss_price along with total_lmp
        - leads to change in format of csv files

AEP did not join PJM until Sep 30, 2004.  I start collecting data at 10/1/04

This code relies upon PJM file naming convention
    - yyyymmdd-da.zip
    - contains
        - yyyymmdd-da.csv
'''

import glob
import os
import csv
import zipfile
import mysql.connector
#from datetime import date, datetime, timedelta
import datetime


def read_lmp_zip(csv_file):

    reportdata = []
    pnode_prices = []
    dst_spring = ['20080309', '20090308', '20100314', '20110313', '20120311', '20130310', '20140309', '20150308', '20160313', '20170312']
    dst_fall = ['20081102', '20091101', '20101107', '20111106', '20121104', '20131103', '20141102', '20151101', '20161106', '20171105']

    full_name = "data/pjm-da.zip"

    myzip = zipfile.ZipFile(full_name)
    myfile = myzip.open(csv_file)
    line_list = myfile.readlines()

    changedate_format_1 = datetime.datetime.strptime('2004-12-01', '%Y-%m-%d')      #added a column for "Type"
    changedate_format_2 = datetime.datetime.strptime('2007-06-01', '%Y-%m-%d')      #added dalily energy rows, congestion_price & marginal_loss_price

    fileyear = csv_file[:4]
    filemonth = csv_file[4:6]
    fileday = csv_file[6:8]
    filedate = datetime.datetime.strptime(fileyear+'-'+filemonth+'-'+fileday, '%Y-%m-%d')
    if filedate < changedate_format_2:
        startrow = 3
    else:
        startrow = 7

    for index, row in enumerate(line_list):

        if index > startrow:
            # convert binary to text and seperate cols
            pnode = row.decode('ascii').split(",")


            if pnode[0] == "End of Day Ahead LMP Data":
                break

            for hour in range(1,25):

                hourly_prices = []

                hourly_prices.append(pnode[0])              #date
                hourly_prices.append("Day Ahead")           #dart
                hourly_prices.append(pnode[1])              #pnode name - old files did not use pnode ID

                hour_ending = "0" + str(hour) + "00"
                hourly_prices.append(hour_ending[-4:])      #hour ending

                if datetime.datetime.strptime(pnode[0], '%Y%m%d') < changedate_format_1:
                    #needs to be converted to float
                    hourly_prices.append(float(pnode[5+hour]))         #total lmp

                elif datetime.datetime.strptime(pnode[0], '%Y%m%d') < changedate_format_2:
                    hourly_prices.append(float(pnode[6+hour]))         #total lmp

                elif csv_file[:8] in dst_spring and hour_ending[-4:] == '0300':
                    hourly_prices.append(0.0)
                    hourly_prices.append(0.0)
                    hourly_prices.append(0.0)

                else:
                    hourly_prices.append(pnode[7+(hour-1)*3])
                    hourly_prices.append(pnode[8+(hour-1)*3])
                    #need to test for data anomoly where extra line feed at hour ending 2400  (10/2/2007)
                    if pnode[9+(hour-1)*3][-2:] == '\n\r':
                        hourly_prices.append(pnode[9+(hour-1)*3][:-2])
                    elif pnode[9+(hour-1)*3][-1:] == '\n':
                        if pnode[9+(hour-1)*3][-2:] == '\r\n':
                            hourly_prices.append(pnode[9+(hour-1)*3][:-2])
                        else:
                            hourly_prices.append(pnode[9+(hour-1)*3][:-1])
                    else:
                        hourly_prices.append(pnode[9+(hour-1)*3])


                pnode_prices.append(hourly_prices)


    # Store prices in lmp table
    cnx = mysql.connector.connect(user='Andrew', password='Kindle01',
                                  host='127.0.0.1',
                                  database='kean')

    cursor = cnx.cursor()

    if filedate < changedate_format_2:
        add_prices = ("INSERT INTO lmp"
                        "(valuation_date, dart, pnode_id, hour_ending, total_lmp) "
                        "VALUES(%s, %s, %s, %s, %s)")
    else:
        add_prices = ("INSERT INTO lmp"
                        "(valuation_date, dart, pnode_id, hour_ending, total_lmp, congestion_price, marginal_loss_price) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s)")
    '''
     Only care about Lightstone plants -- different pnode ids
        - Gavin         32418417, 19
        - PSEGGLOB      32419363, 5, 7 9
        - LawrencC2     32419351, 53, 55, 57, 59, 61
        - Adkins        32418701, 03, 05, 07, 09, 11
        - Ad Hub        34497127

        NEW pnodes -- 3/1/2005
        - Gavin         40243805, 7
        - Adkins        40243919, 21, 23, 25, 27, 29
        - LawrencC2     71856731, 3, 5, 7, 9, 29
        - PSEGGLOB      71856741, 3, 5, 7
    '''

    lightstone_pnodes = ['32418417', '32419363', '32419351', '32418701', '34497127', '40243805', '40243919', '71856731', '71856741']

    for entry in pnode_prices:
        if entry[2] in lightstone_pnodes:
            cursor.execute(add_prices, entry)
            cnx.commit()
#            print(entry)

    cursor.close()

    cnx.close()

    return()
