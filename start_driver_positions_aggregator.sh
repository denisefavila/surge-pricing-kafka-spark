# Start the aggregator consumer (this will block until the consumer stops)
echo "Starting the driver position aggregator..."
python app/driver_position/redis_aggregator_consumer.py