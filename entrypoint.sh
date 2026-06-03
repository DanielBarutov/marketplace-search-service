#!/bin/bash

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting consumer..."
uv run python -m bin.consumer &
CONSUMER_PID=$!

echo "Starting API..."
uv run python -m bin.api &
API_PID=$!

trap "kill $API_PID $CONSUMER_PID; exit 0" SIGINT SIGTERM

while true; do
    kill -0 $API_PID 2>/dev/null
    API_STATUS=$?
    
    kill -0 $CONSUMER_PID 2>/dev/null
    CONSUMER_STATUS=$?
    
    if [ $API_STATUS -ne 0 ] || [ $CONSUMER_STATUS -ne 0 ]; then
        echo "One of the processes has died. Exiting..."
        kill $API_PID $CONSUMER_PID 2>/dev/null
        exit 1
    fi
    sleep 5
done
