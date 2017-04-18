from ftplib import FTP
import sys


def get_file_pjm(filename):

    ftp = FTP('www.pjm.com')
    ftp.login()
    ftp.cwd('pub/account/lmpda')

    #filename = '20170402-da.csv'
    outfile = sys.stdout


    if filename[-4:] == '.zip':
        localfile = open('data/pjm-da.zip', 'wb')
    else:
        localfile = open('data/pjm-da.csv', 'wb')

    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()


def get_file_pjm_rt(filename):

    ftp = FTP('www.pjm.com')
    ftp.login()
    ftp.cwd('pub/account/lmp')

    #filename = '20170402.csv'
    outfile = sys.stdout


    if filename[-4:] == '.zip':
        localfile = open('data/pjm.zip', 'wb')
    else:
        localfile = open('data/pjm-rt.csv', 'wb')

    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()
