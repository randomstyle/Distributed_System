#!/bin/bash

if [ $1 = "server" ]
then
    echo Input host: 
    read host
    echo Input port:
    read port
    python ./server/server.py $host $port
fi

if [ $1 = "client" ]
then
    python ./client/grpc_client.py
fi

if [ $1 = "client_inner" ]
then
    python ./client/grpc_client_inner.py
fi

if [ $1 = "client_inner_internal" ]
then
    echo Input host:port
    read host_port
    python ./client/grpc_client_inner_internal.py $host_port
fi

if [ $1 = "generate" ]
then
    python -m grpc_tools.protoc -I ./proto --python_out=./proto --grpc_python_out=./proto ./proto/inner_data.proto
fi