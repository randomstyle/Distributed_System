import sys
sys.path.append('./proto')

import time
import grpc
import inner_data_pb2
import inner_data_pb2_grpc
import client

from concurrent import futures


import communication_service

def run(host, port, role):
  port = int(port)
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
  ds = communication_service.CommunicationService(role)
  inner_data_pb2_grpc.add_CommunicationServiceServicer_to_server(ds, server)
  server.add_insecure_port('%s:%d' % (host, port))
  server.start()

  _ONE_DAY_IN_SECONDS = 60 * 60 * 24
  try:
    print("Server started at...%d" % port)
    print(host)
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  
  host = sys.argv[1]
  port = int(sys.argv[2])
  role = 'follower'
  if port == 8080:
    role = 'leader'
    print("Leader")
  run(host, port, role)
