from pymongo import MongoClient
from time import time
import logging
import string
import subprocess
import time
import datetime

'''
Mesowest header
'STN YYMMDD/HHMM MNET SLAT SLON SELV TMPF SKNT DRCT GUST PMSL ALTI DWPF RELH WTHR P24I'

Mesonet header
'# id,name,mesonet,lat,lon,elevation,agl,cit,state,country,active'
'''

CONST_MESONET_DELIMITER = ','

CONST_DELIMITER = ','
CONST_NEWLINE_CHAR = '\n'

# station, timestamp_utc, mnet??, latitude, longitude, temperature, ...
#CONST_STD_COL_LIST = CONST_MESOWEST_HEADER.split()
#CONST_MESONET_COL_LIST = ['id','name','mesonet','lat','lon','elevation','agl','cit','state','country','active']

def insert_bulk_mongo(db, data):
    for d in data:
        print d
        values = d.split(',')
        #dateTimeObject = datetime.datetime.strptime(values[1], '%Y%m%d/%H%M')
        #print dateTimeObject
        #pattern = '%Y%m%d/%H%M'
        #time_t = int(time.mktime(time.strptime(values[1], pattern))) * 1000
        #print time_t
        time_t = datetime.datetime.strptime(values[1], '%Y-%m-%d %H:%M:%S')
        input_data = {
            "STN":values[0],
            "timestamp":time_t,
            "MNET":values[2],
            "SLAT":values[3],
            "SLON":values[4],
            "SELV":values[5],
            "TMPF":values[6],
            "SKNT":values[7],
            "DRCT":values[8],
            "GUST":values[9],
            "PMSL":values[10],
            "ALTI":values[11],
            "DWPF":values[12],
            "RELH":values[13],
            "WTHR":values[14],
            "P24I":values[15]
        }
        #print input_data
        result = db.mesowest.insert_one(input_data)
        print 'One post: {0}'.format(result.inserted_id)

def insert_bulk_mongo_mesonet(db, data, timestamp):
    '''
    Mesowest header
    'STN YYMMDD/HHMM MNET SLAT SLON SELV TMPF SKNT DRCT GUST PMSL ALTI DWPF RELH WTHR P24I'

    Mesonet header
    '# id,name,mesonet,lat,lon,elevation,agl,cit,state,country,active'

    Matching:
    # id (0) -> STN
    lat (3) -> SLAT
    long (4) -> SLON
    elevation (5) -> SELV
    '''
    for d in data:
        print d
        values = d.split(',')
        # Convert time from 20180316_2145 to 20180316/2145
        timestamp.replace('_', '/')
        #dateTimeObject = datetime.datetime.strptime(values[1], '%Y%m%d/%H%M')
        #print dateTimeObject
        pattern = '%Y%m%d/%H%M'
        time_t = int(time.mktime(time.strptime(timestamp, pattern))) * 1000
        print time_t
        input_data = {
            "STN":values[0],
            "timestamp":time_t,
            "MNET": "NULL",
            "SLAT":values[3],
            "SLON":values[4],
            "SELV":values[5],
            "TMPF":"NULL",
            "SKNT":"NULL",
            "DRCT":"NULL",
            "GUST":"NULL",
            "PMSL":"NULL",
            "ALTI":"NULL",
            "DWPF":"NULL",
            "RELH":"NULL",
            "WTHR":"NULL",
            "P24I":"NULL"
        }
        #print input_data
        result = db.mesowest.insert_one(input_data)
        print 'One post: {0}'.format(result.inserted_id)

def find_mongo(db, startDate, endDate):
  try:
    print "Finding things"
    print "Start " + startDate
    print "End " + endDate
    pattern = '%Y%m%d/%H%M'
    #startDateTS = int(time.mktime(time.strptime(startDate, pattern))) * 1000
    #endDateTS = int(time.mktime(time.strptime(endDate, pattern))) * 1000
    startDateTS = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
    endDateTS = datetime.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
    print endDateTS
    print startDateTS
    result=db.mesowest.find({"timestamp":{"$lt": endDateTS, "$gte": startDateTS}})
    #for document in result:
    #  print "Result from mongo"
    #  print document
    return result

  except Exception as e:
    logging.warning(e)

def test():
    client = MongoClient('localhost', 27017)
    db = client.pymongo_test

    #data = db.mesowest()
    insert_bulk_mongo(db, )

if __name__ == '__main__':
    fpath = './mesowesteasy.out'
    buffer = []
    with open(fpath) as f:
        for line in f:
            buffer.append(line.rstrip('\n').lstrip(' '))
    print buffer
    client = MongoClient('localhost', 27017)
    db = client.pymongo_test
    insert_bulk_mongo(db, buffer)
    find_mongo(db, '20180316/2100', '20180316/2200')
    #test()
