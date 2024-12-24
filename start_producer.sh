#!/bin/sh

echo "Starting driver position producer..."
python app/driver_position/redis_producer.py &

echo "Starting order producer..."
python app/orders/redis_producer.py &

# Wait for both background processes to finish
wait
