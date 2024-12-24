import logging
import os
import signal

from app.kafka_stream.kafka_producer import (KafkaProducerWrapper,
                                             signal_handler)
from app.orders.generate_data import generate_order

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

shutdown_flag = False

ORDERS_KAFKA_TOPIC = os.getenv("ORDERS_KAFKA_TOPIC", "orders_stream")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Starting Kafka Orders producer...")

    kafka_producer = KafkaProducerWrapper(
        kafka_broker=KAFKA_BROKER,
        topic=ORDERS_KAFKA_TOPIC,
        generate_data_callback=generate_order,
        key_callback=lambda message: message["h3_cell"],
    )
    kafka_producer.produce()
