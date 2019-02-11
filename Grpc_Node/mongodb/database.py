from time import time
import logging
import string
import subprocess
import time

from sql import mesowest_insert_query

insert_query = "insert into mesowest.data (id, station) values ({},'{}');"
select_query = "select {} from {}"

def insert_bulk_mongo(db, data):
  try:
    #create dynamic query and insert into DB
    #TODO need to have a better solution for ID --> primary key
    id = 0
    letter = string.ascii_uppercase
    variable = ['id']
    for d in data:
      id += 1
      values = [id]
      if len(d) == 0:
        continue
      try:
        variable.extend(list(map(lambda x: x[0], d)))
        values.extend(list(map(lambda x: float(x[1]) if str(x[1])[0] not in letter and x[0]!='TIMESTAMP' else
                      (str('\''+str(x[1])+'\'') if x[0]!='TIMESTAMP' else int(x[1])), d ) ))
        mesowestTuple = {
          "id":values[0],
          "STN":values[1],
          "timestamp":values[2],
          "MNET":values[3],
          "SLAT":values[4],
          "SLON":values[5],
          "SELV":values[6],
          "TMPF":values[7],
          "SKNT":values[8],
          "DRCT":values[9],
          "GUST":values[10],
          "PMSL":values[11],
          "ALTI":values[12],
          "DWPF":values[13],
          "RELH":values[14],
          "WTHR":values[15],
          "P24I":values[16]
        }
        #TODO dynamic query assembling needed
        #session.execute(mesowest_insert_query, tuple(values))
        db.mesowest.insert_one(mesowestTuple)
      except Exception as e:
        logging.warning(e)
        continue
    print('finished loading all data')
  except Exception as e:
    logging.error(e)

def insert_bulk_mongo_mesonet(db, data):
  try:
    #create dynamic query and insert into DB
    #TODO need to have a better solution for ID --> primary key
    id = 0
    letter = string.ascii_uppercase
    variable = ['id']
    for d in data:
      id += 1
      values = [id]
      if len(d) == 0:
        continue
      try:
        variable.extend(list(map(lambda x: x[0], d)))
        values.extend(list(map(lambda x: float(x[1]) if str(x[1])[0] not in letter and x[0]!='TIMESTAMP' else
                      (str('\''+str(x[1])+'\'') if x[0]!='TIMESTAMP' else int(x[1])), d ) ))
        mesowestTuple = {
          "id":values[0],
          "STID":values[1],
          "STNM":values[2],
          "timestamp":values[3],
          "RELH":values[4],
          "TAIR":values[5],
          "WSPD":values[6],
          "WVEC":values[7],
          "WDIR":values[8],
          "WDSD":values[9],
          "WSSD":values[10],
          "WMAX":values[11],
          "RAIN":values[12],
          "PRES":values[13],
          "SRAD":values[14],
          "TA9M":values[15],
          "WS2M":values[16],
          "TS10":values[17],
          "TB10":values[18],
          "TS05":values[19],
          "TS25":values[20],
          "TS60":values[21],
          "TR05":values[22],
          "TR25":values[23],
          "TR60":values[24]
        }
        #TODO dynamic query assembling needed
        #session.execute(mesowest_insert_query, tuple(values))
        db.mesowest.insert_one(mesowestTuple)
      except Exception as e:
        logging.warning(e)
        continue
    print('finished loading all data')
  except Exception as e:
    logging.error(e)

def find_mongo(db, startDate, endDate):
  try:
    pattern = '%Y%m%d/%H%M'
    startDateTS = int(time.mktime(time.strptime(startDate, pattern))) * 1000
    endDateTS = int(time.mktime(time.strptime(endDate, pattern))) * 1000
    result=db.mesowest.find({"timestamp":{"$lt": endDateTS, "$gte": startDateTS}})
    for document in result:
      print "Result from mongodb"
      print(document)
    return result

  except Exception as e:
    logging.warning(e)

def find_dates():
  return db.mesowest.distinct("timestamp")
