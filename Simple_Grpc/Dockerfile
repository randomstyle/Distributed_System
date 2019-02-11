FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y software-properties-common vim \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv \
    && apt-get install -y git

# Update pip
RUN python3.6 -m pip install pip --upgrade && python3.6 -m pip install wheel

# RocksDB
RUN apt-get install -y libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev \
    && git clone https://github.com/facebook/rocksdb.git \
    && cd rocksdb \
    && git reset --hard 8d7926a766f2ab9bd6e7aa8cba80b5d3ff26c52b \
    && export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:`pwd` \
    && make shared_lib \
    && make install-shared INSTALL_PATH=/usr
RUN pip install pyrocksdb

# gRPC @https://github.com/grpc/grpc-docker-library/blob/master/1.4/python/Dockerfile
ENV GRPC_PYTHON_VERSION 1.4.0
RUN pip install grpcio==${GRPC_PYTHON_VERSION} grpcio-tools==${GRPC_PYTHON_VERSION}

CMD ["python3.6"]


