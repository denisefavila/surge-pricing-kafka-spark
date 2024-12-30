import logging
import os
import signal

from app.driver_position.generate_data import generate_driver_position
from app.kafka_stream.kafka_producer import (KafkaProducerWrapper,
                                             signal_handler)
from app.logging_utils import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

shutdown_flag = False

DRIVER_POSITION_KAFKA_TOPIC = os.getenv(
    "DRIVER_POSITION_KAFKA_TOPIC", "driver_position_stream"
)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Starting Kafka DriverPosition producer...")

    kafka_producer = KafkaProducerWrapper(
        kafka_broker=KAFKA_BROKER,
        topic=DRIVER_POSITION_KAFKA_TOPIC,
        generate_data_callback=generate_driver_position,
        key_callback=lambda message: message["h3_cell"],
    )
    kafka_producer.produce()
