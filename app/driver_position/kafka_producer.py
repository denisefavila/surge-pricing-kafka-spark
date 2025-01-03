import logging
import os
import signal

from app.driver_position.driver_position_simulator import \
    DriverPositionSimulator
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

simulator = DriverPositionSimulator()
simulator.initialize_positions()


def generate_data():
    """Callback to generate data for KafkaProducer."""
    return simulator.update_position()


def generate_key(data):
    """Callback to generate a key for Kafka partitioning."""
    return str(data["h3_cell"])


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Starting Kafka DriverPosition producer...")

    kafka_producer = KafkaProducerWrapper(
        kafka_broker=KAFKA_BROKER,
        topic=DRIVER_POSITION_KAFKA_TOPIC,
        generate_data_callback=generate_data,
        key_callback=generate_key,
    )
    kafka_producer.produce()
