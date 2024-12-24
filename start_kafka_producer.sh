#!/bin/sh

echo "Starting driver position producer..."
python app/driver_position/kafka_producer.py &

echo "Starting order producer..."
python app/orders/kafka_producer.py &

# Wait for both background processes to finish
wait
