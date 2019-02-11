### Requirements

Implement a key-value store gRPC service using [RocksDB](https://pypi.python.org/pypi/python-rocksdb).

### Running Python scripts via Docker

* RocksDB native - https://github.com/facebook/rocksdb/blob/master/INSTALL.md
* gRPC Docker - https://github.com/grpc/grpc-docker-library/tree/master/1.4/python

OR

Create a Docker image using [this example](https://github.com/sithu/cmpe273-fall17/tree/master/docker).

* Create a Docker network so that each container can connect to the host under the fixed IP 192.168.0.1.

```sh
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
```

* Run the server and client containers.

```sh
# Generate Stub for client and server
docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto


# Server
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

# Client
docker run -it --rm --name lab1-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1
```

### Expected Output on Client

```sh
Client is connecting to Server at 192.168.0.1:3000...
## PUT Request: value = foo
## PUT Response: key = 3f8a2ec27bc44423ba2488801cfa1b94
## GET Request: key = 3f8a2ec27bc44423ba2488801cfa1b94
## GET Response: value = foo
```