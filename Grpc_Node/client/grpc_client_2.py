import sys
sys.path.append('./proto')

import uuid, time, argparse, socket, fcntl, struct
import requests
import grpc
import inner_data_pb2_grpc
from inner_data_pb2 import Request, Response, PingRequest, PutRequest, GetRequest, DatFragment, MetaData, QueryParams

CONST_MEDIA_TYPE_TEXT_MESOWEST = 1

# Looks like 1KB is a good chunk size
CONST_CHUNK_SIZE = 1  # number of lines per payload

CONST_MESOWEST_HEADER = 'STN YYMMDD/HHMM MNET SLAT SLON SELV TMPF SKNT DRCT GUST PMSL ALTI DWPF RELH WTHR P24I'

nodes = requests.get('https://cmpe275-spring-18.mybluemix.net/get').text.split(',')
# my_ip = get_ip_address('eth0')
my_ip = '169.254.176.49'

# TODO: yield timestamp for mesonet data
def preprocess(fpath):
  """read file and chunkify it to be small batch for grpc transport

  Returns: a string, concat of data rows, separated by newline char
  """
  buffer = []
  is_starts_reading = False
  is_mesonet = False
  with open(fpath) as f:
    for line in f:
      print line
      # mesowest
      if ' '.join(line.strip().split()) == CONST_MESOWEST_HEADER:
        is_starts_reading = True
        # skip this line
        continue
      # TODO: for mesonet
      elif False:
        is_starts_reading = True
        is_mesonet = True
      if not is_starts_reading:
        continue
      if len(buffer) == CONST_CHUNK_SIZE:
        res = ''.join(buffer)
        buffer = []
        yield res
      else:
        # we can't call strip() here as it will remove the newline char
        buffer.append(line)
    # last batch
    if buffer:
      yield ''.join(buffer)

def put_req_iterator(fpath, sender, receiver):
  my_uuid = str(uuid.uuid1())
  for raw in preprocess(fpath):
    print 'raw data'
    print raw
    yield Request(
      fromSender=sender,
      toReceiver=receiver,
      putRequest=PutRequest(
          metaData=MetaData(uuid=my_uuid, mediaType=CONST_MEDIA_TYPE_TEXT_MESOWEST),
          datFragment=DatFragment(data=raw.encode()))
      )

class Client():
  def __init__(self, host, port, sender):
    assert sender is not None, 'sender has to be specified'
    self.channel = grpc.insecure_channel('%s:%d' % (host, port))
    self.stub = inner_data_pb2_grpc.CommunicationServiceStub(self.channel)
    self.sender = sender
    self.receiver = host

  def ping(self, msg):
    """
    Returns: bool
    """
    req = Request(
      fromSender=self.sender,
      toReceiver=self.receiver,
      ping=PingRequest(msg=msg))
    resp = self.stub.ping(req)
    print(resp.msg)
    return True

  def put(self, fpath):
    """
    Returns: bool
    """
    req_iterator = put_req_iterator(fpath, self.sender, self.receiver)
    resp = self.stub.putHandler(req_iterator)
    print(resp.msg)
    if resp.Code == 2:
      print('write failed at this node!')
      return False
    return True

  def get(self, fp, from_utc, to_utc):
    """
    Returns: bool
    """
    req = Request(
      fromSender=self.sender,
      toReceiver=self.receiver,
      getRequest=GetRequest(
          metaData=MetaData(uuid='14829'),
          queryParams=QueryParams(from_utc=from_utc,to_utc=to_utc))
      )
    for resp in self.stub.getHandler(req):
      if resp.code == 2:
        print('read failed at this node!')
        return False
      else:
        fp.write(resp.datFragment.data.decode())

    return True

def main():
  """
  Sample Usage:
  get: -H 0.0.0.0 -P 8080 -g -t '2016-07-08 10:00:00' '2016-07-08 10:00:00'
  put: -H 0.0.0.0 -P 8080 -u -f './201803180010.mdf'
  ping: -H 0.0.0.0 -P 8080 -p -m 'hello world!'
  """
  parser = argparse.ArgumentParser(description='Weather Data Lake Python API v1.0')
  parser.add_argument('-H', '--host', type=str, default='0.0.0.0', help='The host of the grpc server')
  parser.add_argument('-P', '--port', type=int, default=8080, help='The port listened by grpc server')
  parser.add_argument('-f', '--file', type=str, default='../mesowesteasy.out', help='The file path to upload')
  parser.add_argument('-g', '--get', action='store_true', default=False, help='-g -t <from_utc> <to_utc>')
  parser.add_argument('-u', '--upload', action='store_true', default=False, help='Upload data to the server')
  parser.add_argument('-p', '--ping', action='store_true', default=False, help='Ping the server')
  parser.add_argument('-t', '--range', type=str, nargs=2, help='-t <from_utc> <to_utc>')
  parser.add_argument('-s', '--stations', nargs='*', help='-s <station1> <station2> <...>')
  parser.add_argument('-m', '--message', type=str, default='Hello World!', help='-m "Hello World!"')
  parser.add_argument('-o', '--output', type=str, default='./result.out', help='-m "Specify the output file locaton for queries"')

  args = parser.parse_args()
  try:
    host = args.host
    port = args.port
    assert host
    assert port
    client = Client(host, port, my_ip)
    if args.get:
      assert args.range
      from_utc, to_utc = args.range[0], args.range[1]
      assert from_utc
      assert to_utc
      with open(args.output, 'w') as fp:
        if not client.get(fp, from_utc=from_utc, to_utc=to_utc):
          for node in nodes:
            client = Client(node, port, host)
            if client.get(fp, from_utc=from_utc, to_utc=to_utc):
              print('get succeeded at one of the other nodes')
              break
          print('get failed at all other nodes')
        else:
          print('get succeeded at this node')

    elif args.upload:
      fp = args.file
      assert fp
      if not client.put(fpath=fp):
        for node in nodes:
          client = Client(node, port, host)
          if client.put(fpath=fp):
            print('put succeeded at one of the other nodes')
            break
        print('put failed at all other nodes')
      else:
        print('put succeeded at this node')

    elif args.ping:
      client.ping(msg=args.message)
  except Exception as e:
    print(e)
    parser.print_help()


if __name__ == '__main__':
  main()
