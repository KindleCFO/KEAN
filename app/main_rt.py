'''
Smarter code would not need hard test for file extensions.

TODO
    - add altered pnodes
        - made some changes midstream (Gavin, Adkins) but will need to fill in for early dates post conversion
        - need to determine new pnodes for Lawrenceburg and Waterford
        - check for duplicate records around 2010-12-07 and 2016-05-12
    - add unique key to lmp table (valuation_date, pnode, hour_ending)
    - fix fall DST
        - correct current labeling (0300 happens twice but shows HE 0400)
        - add additional record for additional hour
    - How do we know if we have a good data set?
'''

#from read_zip import read_lmp_zip
from read_csv_rt import read_lmp_csv_rt
from scraping import get_file_pjm_rt

import datetime


startdate = datetime.datetime.strptime('2017-01-17', '%Y-%m-%d')

changedate_csv = datetime.datetime.strptime('2017-01-17', '%Y-%m-%d')   #date files change to .csv

#endcount = (datetime.datetime.strptime('2017-01-12', '%Y-%m-%d') - startdate).days + 1     #use for specific date end
endcount = (datetime.datetime.today()-startdate).days + 1

for day in range(0, endcount):          #13 years of data

    filedate = startdate + datetime.timedelta(days=day)

    if filedate < changedate_csv:
        extension = '.zip'
    else:
        extension = '.csv'

    fileyear = str(filedate.year)
    filemonth = '0' + str(filedate.month)
    fileday = '0' + str(filedate.day)

    filename = fileyear + filemonth[-2:] + fileday[-2:] + extension

    #get file from pjm-da
    get_file_pjm_rt(filename)

    #reade file, laod into kean
    zipped_csv_filename = filename[:-3] + 'csv'

    if filedate < changedate_csv:
        read_lmp_zip_rt(zipped_csv_filename)
    else:
        read_lmp_csv_rt()
