'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse
import time
import rocksdb
PORT = 3000

class DatastoreClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.db = rocksdb.DB("lab2.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)
        self.count = 0

    def connect_server(self, value):
        return self.stub.connect_server(datastore_pb2.RequestSequence(data=value))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = DatastoreClient(host=args.host)
    
    while True:
        resp = client.connect_server(client.count)
        for rr in resp:
            op = rr.data.split(',')
            client.count += 1
            if op[0] == 'put':
                client.db.put(op[1].encode(), op[2].encode())
                print('put ' + op[1] + ' ' + client.db.get(op[1].encode()).decode())
            else:
                client.db.delete(op[1].encode())
                print('delete ' + op[1])
        time.sleep(1)

if __name__ == "__main__":
    main()