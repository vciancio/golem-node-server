#!/bin/bash
echo "Setting up Golem Node w/ path='$1'"

docker run --rm \
    -v $1/ya-provider:/root/.local/share/ya-provider:rw \
    -v $1/yagna:/root/.local/share/yagna:rw \
    -it vciancio/golem-node-server:latest \
    golemsp run