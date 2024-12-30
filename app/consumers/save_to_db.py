import json
import logging

from dotenv import load_dotenv
from kafka import KafkaConsumer

from cassandra_db.cassandra_connection import create_cassandra_connection

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class KafkaConsumerWrapper:
    def __init__(self, kafka_broker, topic, cassandra_table, group_id=None):
        """
        A Kafka consumer that consumes messages from a Kafka topic and saves them to a Cassandra database.

        Args:
            kafka_broker: Kafka broker address (e.g., localhost:9092).
            topic: The Kafka topic to consume messages from.
            cassandra_table: The Cassandra table where data should be inserted.
        """
        self.topic = topic
        self.cassandra_table = cassandra_table
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=kafka_broker,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            group_id=group_id,
            api_version=(0, 10),
        )

        self.session = create_cassandra_connection()

    def consume(self):
        """Continuously consume messages and insert them into the specified Cassandra table."""
        for message in self.consumer:
            data = message.value
            logger.info(f"Consumed data: {data}")

            try:
                insert_query = f"""
                    INSERT INTO {self.cassandra_table} (id, data)
                    VALUES (uuid(), %s)
                """
                self.session.execute(insert_query, (json.dumps(data),))
                logger.info(f"Data inserted into {self.cassandra_table}.")
            except Exception as e:
                logger.error(f"Failed to insert data into {self.cassandra_table}: {e}")
