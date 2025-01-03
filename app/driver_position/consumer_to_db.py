import logging

from app.driver_position.kafka_consumer_to_db import DriverPositionConsumer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    kafka_broker = "kafka:29092"
    kafka_topic = "driver_position_stream"

    # Create and start the consumer
    consumer = DriverPositionConsumer(kafka_broker, kafka_topic)
    consumer.consume()
