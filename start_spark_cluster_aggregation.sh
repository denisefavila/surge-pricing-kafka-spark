#!/bin/sh

echo "Starting driver position aggregator..."
python app/driver_position/kafka_stream_aggregator.py &

# Wait for both background processes to finish
wait
