import os

from app.kafka_stream.structures_streaming import KafkaStructuredStreaming

if __name__ == "__main__":
    ORDERS_KAFKA_TOPIC = os.getenv("ORDERS_KAFKA_TOPIC", "orders_stream")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

    # Initialize KafkaStructuredStreaming with Redis settings
    kafka_streaming = KafkaStructuredStreaming(
        app_name="KafkaStructuredStreaming",
        kafka_broker=KAFKA_BROKER,
        topic=ORDERS_KAFKA_TOPIC,
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
    )

    # Read data from Kafka topic
    kafka_df = kafka_streaming.read_from_kafka()

    # Parse the Kafka data using the predefined schema
    parsed_df = kafka_streaming.parse_data(kafka_df)

    # Aggregate the parsed data
    aggregated_df = kafka_streaming.aggregate_data(parsed_df)

    query = kafka_streaming.save_to_redis(aggregated_df)

    query.awaitTermination()
