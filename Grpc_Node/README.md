# PYTHON2 ONLY
# Download
pip install grpcio-tools  
pip install grpcio  
mongodb  
pymongo  

# How to run (since i only have 1 laptop, i use different port number to run servers)
### 1. Generate proto code
bash proto.sh generate

### 2. Run server 1 at 8080 (dont change port number I hardcoded it)
bash proto.sh server  
input 0.0.0.0 for host hit enter  
input 8080 for port hit enter  

### 3. Run server 2 at 8081 (dont change port number I hardcoded it)
bash proto.sh server  
input 0.0.0.0 for host hit enter  
input 8081 for port hit enter  

### 4. Run inner client (this is for leader election. This is a client that send heartbeat to the leader server 8080. I haven't finished leader election yet for now just heartbeat)
bash proto.sh client_inner

### 5. Run client (this will be the real client it will send a put request to the leader server at 8080)
bash proto.sh client

### What you should see
a string of json print out in the 8081 server terminal (indicate that the put request was sent successfully from 8080 to 8081)
