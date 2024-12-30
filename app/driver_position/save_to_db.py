import logging
import os
import uuid
from datetime import datetime

from app.consumers.save_to_db import KafkaConsumerWrapper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


CASSANDRA_DRIVER_POSITION_TABLE = os.getenv(
    "CASSANDRA_DRIVER_POSITION_TABLE", "driver_position"
)

GROUP_ID = "driver_position_group"


class DriverPositionConsumer(KafkaConsumerWrapper):
    def __init__(
        self,
        kafka_broker,
        topic,
        group_id=GROUP_ID,
        cassandra_table=CASSANDRA_DRIVER_POSITION_TABLE,
    ):
        """
        A Kafka consumer specifically for consuming driver position data and saving it to the 'driver_position' table.

        Args:
            kafka_broker: Kafka broker address (e.g., localhost:9092).
            topic: The Kafka topic to consume messages from.
            cassandra_table: The Cassandra table to insert driver position data into.
        """
        super().__init__(kafka_broker, topic, cassandra_table, group_id)

    def consume(self):
        """Continuously consume driver position messages and insert them into the driver_position table."""
        for message in self.consumer:
            data = message.value
            logger.info(f"Consumed driver position data: {data}")

            try:
                # Assuming the data contains fields: driver_id, latitude, longitude, and timestamp
                insert_query = f"""
                    INSERT INTO {self.cassandra_table} (driver_id, latitude, longitude, timestamp)
                    VALUES (%s, %s, %s, %s)
                """

                driver_id = uuid.UUID(data.get("driver_id"))
                latitude = float(data.get("latitude"))
                longitude = float(data.get("longitude"))
                timestamp = datetime.strptime(
                    data.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%f"
                )

                self.session.execute(
                    insert_query, (driver_id, latitude, longitude, timestamp)
                )
                logger.info(
                    f"Driver position data inserted into {self.cassandra_table}."
                )
            except Exception as e:
                logger.error(
                    f"Failed to insert driver position data into {self.cassandra_table}: {e}"
                )
