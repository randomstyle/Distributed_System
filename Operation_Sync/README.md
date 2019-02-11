### Setup

Similar to Simple_Grpc  

### Run

Create client and server stub and run server, client similar to lab1  

Run test.py after running server.py and client.py  
docker run -it --rm --name lab2-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 test.py 192.168.0.1

### Expect output after running test.py

In both server and client bash these two line appear  
put fe6afe74e7374cb8a22289535c971ae7 trung  
delete fe6afe74e7374cb8a22289535c971ae7  