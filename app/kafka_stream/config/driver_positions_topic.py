import os

from app.kafka_stream.config.settings import create_kafka_topic

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")


if __name__ == "__main__":
    create_kafka_topic(
        topic_name="driver_position_stream",
        num_partitions=3,
        replication_factor=1,
        bootstrap_servers="localhost:9092",
    )
