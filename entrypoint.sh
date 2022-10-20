#!/usr/bin/env bash

EMBEDED_DB=${EMBEDED_DB:-}

if [ -n "$EMBEDED_DB" ]; then
    echo "[*] Starting embedded MongoDB database"
    /usr/local/mongodb/bin/mongod --dbpath /data/db/mongo 2> /dev/null > /dev/null &
    sleep 5

    echo "[*] Starting embedded Redis database"
    redis-server 2> /dev/null > /dev/null &

    export MONGO_URI=mongodb://127.0.0.1:27017
    export REDIS_URI=redis://127.0.0.1:6379/0

fi

echo "[*] Creating MongoDB Indexes"
export FLASK_APP=easy_logs.app

flask create-mongo-indexes

echo "[*] Starting EasyLogs"
exec gunicorn --bind :8080 -w 10 --worker-class gevent --timeout 0 --backlog 1024 --worker-connections 512 easy_logs.app:app
