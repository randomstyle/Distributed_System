'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import rocksdb
import asyncio
import signal
import threading
from concurrent import futures


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def decorator(op):

    def wrapper(self, request, context):
        key = op(self, request, context)
        self.history.append(op.__name__ + ',' + key + ',' + request.data)
        return datastore_pb2.Response(data=key)

    return wrapper

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("lab1.db", rocksdb.Options(create_if_missing=True))
        self.history = []

    @decorator
    def put(self, request, context):
        key = uuid.uuid4().hex
        print('put ' + key + ' ' + request.data)
        self.db.put(key.encode(), request.data.encode())
        return key

    @decorator
    def delete(self, request, context):        
        self.db.delete(request.data.encode())
        print("delete " + request.data)
        return request.data

    def connect_server(self, request, context):
        for item in self.history[request.data:]:
            yield datastore_pb2.Response(data=item)
            
def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()
    
    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run('0.0.0.0', 3000)
