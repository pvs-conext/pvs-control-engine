#!/usr/bin/env bash

THIS_SCRIPT_FILE_MAYBE_RELATIVE="$0"
THIS_SCRIPT_DIR_MAYBE_RELATIVE="${THIS_SCRIPT_FILE_MAYBE_RELATIVE%/*}"
THIS_SCRIPT_DIR_ABSOLUTE=`readlink -f "${THIS_SCRIPT_DIR_MAYBE_RELATIVE}"`

sudo apt-get --yes install autoconf automake libtool curl make g++ unzip
sudo apt-get --yes install zlib1g-dev
sudo apt-get --yes install pkg-config
sudo apt-get --yes install libpcap-dev python-libpcap

# Protobuf
git clone https://github.com/google/protobuf.git
cd protobuf
git checkout v3.6.1
export CFLAGS="-Os"
export CXXFLAGS="-Os"
export LDFLAGS="-Wl,-s"
./autogen.sh
./configure
make clean
make
sudo make install
sudo ldconfig
unset CFLAGS CXXFLAGS LDFLAGS
cd python
sudo python setup.py install
cd ../..

git clone https://github.com/grpc/grpc.git

cd grpc
git checkout v1.17.2
git submodule update --init --recursive
export LDFLAGS="-Wl,-s"
make clean
make
sudo make install
sudo ldconfig
unset LDFLAGS
cd ..

# Deps needed to build PI:
sudo apt-get --yes install libjudy-dev libreadline-dev valgrind libtool-bin libboost-dev libboost-system-dev libboost-thread-dev

# PI/P4Runtime
git clone https://github.com/p4lang/PI.git
cd PI
git submodule update --init --recursive
cp ../proto/p4runtime.proto proto/p4runtime/proto/p4/v1
./autogen.sh
./configure --with-proto
make
sudo make install
sudo ldconfig
cd ..

sudo python -m pip install grpcio
sudo python -m pip install grpcio-tools
sudo python -m pip uninstall protobuf
sudo python -m pip install protobuf
