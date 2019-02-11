import uuid
import grpc
import data_pb2_grpc
from data_pb2 import Request, Response, PingRequest, PutRequest, GetRequest, DatFragment, MetaData, QueryParams

import argparse
from datetime import datetime, timedelta
import time

CONST_MEDIA_TYPE_TEXT = 1
CONST_CHUNK_SIZE = 2  # number of lines per payload
CLIENT_IP = '0.0.0.0'

def preprocess(fpath):
    """read file and chunkify it to be small batch for grpc transport"""
    #timestamp_utc = '2017-08-08 12:00:00'
    cnt = 10
    buffer = []
    with open(fpath) as f:
        for line in f:
            print line
            if not cnt:
                break
            if len(buffer) == CONST_CHUNK_SIZE:
                print "Chunk size"
                res = ''.join(buffer)
                buffer = []
                print "Res is"
                print res
                putRequest=PutRequest(
                    metaData=MetaData(uuid='14829', mediaType=CONST_MEDIA_TYPE_TEXT),
                    datFragment=DatFragment(data=res.encode()))
                request = Request(
                    fromSender='some put sender',
                    toReceiver='some put receiver',
                    putRequest=putRequest
                )
                yield res
            else:
                buffer.append(line)
            cnt = cnt - 1
        if buffer:
            yield ''.join(buffer)

def process_file(fpath):
    buffer = []
    with open(fpath) as f:
        for line in f:
            buffer.append(line.rstrip('\n').lstrip(' '))
    return buffer

def put_iterator(fpath, timestamp = ''):
    buffer = process_file(fpath)
    for raw in buffer:
        if timestamp != '':
            data_out = normalize_data_mesonet(raw, timestamp)
            print data_out
        else:
            data_out = normalize_data_mesowest(raw)
        putRequest=PutRequest(
            metaData=MetaData(uuid='14829', mediaType=CONST_MEDIA_TYPE_TEXT),
            datFragment=DatFragment(data=data_out.encode(), timestamp_utc=timestamp))
        request = Request(
            fromSender=CLIENT_IP,
            toReceiver='host IP',
            putRequest=putRequest
        )
        yield request


def normalize_data_mesonet(input, timestamp):
    MESONET_STR = '%s,%s,NULL,%s,%s,%s,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL'
    #print 'Before ' + timestamp
    timestamp = timestamp.replace('_', '/')
    #print 'After ' + timestamp
    date_obj = datetime.strptime(timestamp, '%Y%m%d/%H%M')
    time_s = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')
    #print time_s
    output = ''
    #print input
    values = input.split(',')
    #pattern = '%Y%m%d/%H%M'
    #time_t = int(time.mktime(time.strptime(timestamp, pattern))) * 1000
    #dt = .strftime('%Y-%m-%d %H:%M:%S')
    #print(dt)
    output = MESONET_STR % (values[0], time_s, values[3], values[4], values[5])
    #print 'Output is ' + output
    return output

def normalize_data_mesowest(input):
    MESOWEST_STR = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'
    pattern = '%Y%m%d/%H%M'
    print input
    values = input.split()
    date_obj = datetime.strptime(values[1], '%Y%m%d/%H%M')
    time_s = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')
    #pattern = '%Y%m%d/%H%M'
    #time_t = int(time.mktime(time.strptime(values[1], pattern))) * 1000
    output = MESOWEST_STR % (values[0], time_s, values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12], values[13], values[14], values[15])
    print "Output is " + output
    return output

class Client():
  def __init__(self, host='0.0.0.0', port=8080):
    self.receiver_ip = host
    self.channel = grpc.insecure_channel('%s:%d' % (host, port))
    self.stub = data_pb2_grpc.CommunicationServiceStub(self.channel)

  def ping(self, data):
    req = Request(
      fromSender=CLIENT_IP,
      toReceiver=self.receiver_ip,
      ping=PingRequest(msg='this is a sample ping request'))
    resp = self.stub.ping(req)
    return resp.msg


  def put(self, fpath):
    my_uuid = str(uuid.uuid1())
    #req = preprocess(fpath)
    req = process_file(fpath)
    request_iterator = put_iterator(fpath)

    resp = self.stub.putHandler(request_iterator)
    print("Response code " + resp.Code)
    print(resp.msg)
    #return True

  def put_mesonet(self, fpath):
    my_uuid = str(uuid.uuid1())
    #req = preprocess(fpath)
    req = process_file(fpath)
    request_iterator = put_iterator(fpath, '20050621_0800')

    resp = self.stub.putHandler(request_iterator)
    print("Response code " + str(resp.Code))
    print(resp.msg)
    #return True

  def get(self):
    req = Request(
      fromSender=CLIENT_IP,
      toReceiver=self.receiver_ip,
      getRequest=GetRequest(
          metaData=MetaData(uuid='14829'),
          queryParams=QueryParams(from_utc='2018-03-16 21:00:00',to_utc='2018-03-16 23:00:00'))
      )
    resp = self.stub.getHandler(req)
    print 'Response from server'
    for response in resp:
    	print response
        print response.datFragment.data
    #print resp.msg
    #return resp.datFragment.data

def test():
  client = Client()

  print(client.ping('hello'))
  print(client.put('./mesowesteasy.out'))
  print(client.put_mesonet('./mesonettest.csv'))
  #print(client.ping())


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--foo', help='foo help')
  parser.add_argument('--ping', help='ping someone', action="store_true")
  parser.add_argument('-x', '--host', help='server host')
  parser.add_argument('-p', '--port', type = int, help='server port')
  parser.add_argument('--put', help='put a file to server')
  parser.add_argument('--get', help='get data from server to a file')
  parser.add_argument('-t', '--test', help='test command', action="store_true")
  args = parser.parse_args()

  if args.host:
      host = args.host
  else:
      host = '0.0.0.0'

  if args.port:
      port = args.port
  else:
      port = 8080

  client = Client(host=host, port=port)
  if args.ping:
      print(client.ping('hello'))
  if args.put:
      filename = args.put
      if filename.endswith('.csv'):
          #mesonet
          print(client.put_mesonet(filename))
      else:
          #mesowest
          print(client.put(filename))
  if args.get:
      filename = args.get
      print(client.get())

  if args.test:
      test()
  #test()
