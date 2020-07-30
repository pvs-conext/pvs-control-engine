#!/bin/bash

set -xe

# cleanup
rm -rf database.db

source scripts/export_vars.sh

# run server. check config/ServerConfig.py for settings
python server/grpc_server.py
