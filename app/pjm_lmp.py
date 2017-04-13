from ftplib import FTP
import sys


#ftp = FTP('ftp://ftp.cmegroup.com')
ftp = FTP('www.pjm.com')
ftp.login()
ftp.cwd('pub/account/lmpda')

#print(ftp.dir())

filename = '20170402-da.csv'
outfile = sys.stdout

localfile = open('data/pjm-da.csv', 'wb')
ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

ftp.quit()
'''

def grabFile():

    filename = 'stlags'

    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR' + filename, localfile.write, 1024)

    ftpquit()
    localfile.close

'''
