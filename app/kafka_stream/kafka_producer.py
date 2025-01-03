import json
import logging
import os
import signal
import time

from dotenv import load_dotenv
from kafka import KafkaProducer

from app.logging_utils import setup_logging

load_dotenv()

PRODUCE_INTERVAL = float(os.getenv("PRODUCE_INTERVAL", 1.0))
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "default_topic")

setup_logging()

logger = logging.getLogger(__name__)

shutdown_flag = False


def signal_handler(sig, frame):
    global shutdown_flag
    logger.info("Shutdown signal received. Stopping producer...")
    shutdown_flag = True


class KafkaProducerWrapper:
    def __init__(self, kafka_broker, topic, generate_data_callback, key_callback=None):
        """
        A general Kafka producer that sends data to a Kafka topic.

        Args:
            kafka_broker: Kafka broker address (e.g., localhost:9092).
            topic: The Kafka topic name.
            generate_data_callback: A function that generates data for the topic.
            key_callback: A function that generates the key for Kafka partitioning. Defaults to None.
        """
        self.topic = topic
        self.generate_data_callback = generate_data_callback
        self.key_callback = key_callback  # New parameter for key generation

        # Configure the Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: str(k).encode("utf-8") if k else None,
            api_version=(0, 10),
        )

    def produce(self):
        """Continuously produce data and send it to the Kafka topic."""
        global shutdown_flag
        try:
            while not shutdown_flag:
                schema = self.generate_data_callback()
                if not schema:
                    continue
                data = schema.to_dict()
                key = self.key_callback(data) if self.key_callback else None

                try:
                    # Send the message with the key
                    self.producer.send(self.topic, value=data, key=key)
                    logger.info(
                        f"Data sent to topic {self.topic}: {data} with key: {key}"
                    )
                except Exception as e:
                    logger.error(f"Failed to send data to Kafka: {e}")
                    time.sleep(PRODUCE_INTERVAL * 2)

                time.sleep(PRODUCE_INTERVAL)

        except Exception as e:
            logger.exception(f"Unexpected error in producer: {e}")
        finally:
            self.producer.close()
            logger.info("Producer stopped.")
