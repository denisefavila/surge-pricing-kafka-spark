#!/bin/sh

echo "Starting driver position producer..."
python app/driver_position/consumer_to_db.py &

# Wait for both background processes to finish
wait
