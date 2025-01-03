import os
import uuid
from datetime import datetime

from app.consumers.save_to_db import KafkaConsumerWrapper
from app.logging_utils import setup_logging, setup_structured_logger

ELASTICSEARCH_DRIVER_POSITION_INDEX = os.getenv(
    "ELASTICSEARCH_DRIVER_POSITION_INDEX", "driver_position_logs"
)

# Cassandra table and Kafka settings
CASSANDRA_DRIVER_POSITION_TABLE = os.getenv(
    "CASSANDRA_DRIVER_POSITION_TABLE", "driver_position"
)
GROUP_ID = "driver_position_group"


logger = setup_structured_logger(ELASTICSEARCH_DRIVER_POSITION_INDEX)
application_logger = setup_logging()


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
            application_logger.info(f"Consumed driver position data: {data}")

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
                    "[DriverPosition] Sent",
                    extra={
                        "driver_id": str(driver_id),
                        "location": {"lat": latitude, "lon": longitude},
                        "timestamp": timestamp.isoformat(),
                    },
                )

            except Exception as e:
                application_logger.error(
                    f"Failed to insert driver position data into {self.cassandra_table}: {e}"
                )
