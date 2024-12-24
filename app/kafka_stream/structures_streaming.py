from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window
from pyspark.sql.types import (FloatType, StringType, StructField, StructType,
                               TimestampType)

from app.redis_stream.redis_client import redis_client


class KafkaStructuredStreaming:
    def __init__(
        self, app_name, kafka_broker, topic, redis_host="redis", redis_port=6379
    ):
        """
        Initialize the KafkaStructuredStreaming class with Spark session and Kafka parameters.
        """
        self.app_name = app_name
        self.kafka_broker = kafka_broker
        self.topic = topic
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.spark = (
            SparkSession.builder.appName(self.app_name)
            .config("spark.redis.host", self.redis_host)
            .config("spark.redis.port", self.redis_port)
            .getOrCreate()
        )

        self.schema = StructType(
            [
                StructField("driver_id", StringType(), True),
                StructField("latitude", FloatType(), True),
                StructField("longitude", FloatType(), True),
                StructField("timestamp", TimestampType(), True),
                StructField("h3_cell", StringType(), True),
            ]
        )

    def read_from_kafka(self):
        """
        Read data from Kafka topic as a streaming DataFrame.
        """
        return (
            self.spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", self.kafka_broker)
            .option("subscribe", self.topic)
            .load()
        )

    def parse_data(self, df):
        """
        Parse Kafka data using the predefined schema.
        """
        kafka_data = df.selectExpr("CAST(value AS STRING)", "timestamp")
        return kafka_data.select(
            from_json(col("value"), self.schema).alias("data"), "timestamp"
        )

    @staticmethod
    def aggregate_data(parsed_data):
        """
        Perform aggregation on parsed data.
        """
        aggregated_data = parsed_data.groupBy("data.h3_cell").count()
        return aggregated_data

    @staticmethod
    def windowed_aggregation(parsed_data):
        """
        Perform windowed aggregation based on driver_id and a time window.
        """
        windowed_data = parsed_data.groupBy(
            window("timestamp", "5 minutes"), "data.h3_cell"
        ).count()
        return windowed_data

    @staticmethod
    def write_to_console(data, output_mode="complete"):
        """
        Write aggregated data to the console.
        """
        query = data.writeStream.outputMode(output_mode).format("console").start()
        return query

    def save_to_redis(self, aggregated_data):
        """
        Save the aggregated data to Redis.
        """

        def write_to_redis(batch_df, batch_id):
            """
            Function to write a batch of data to Redis.
            """
            with redis_client(
                redis_host=self.redis_host, redis_port=self.redis_port
            ) as client:
                for row in batch_df.collect():
                    h3_cell = row["h3_cell"]
                    value = row.asDict()  # Convert the row to a dictionary
                    # Store data in Redis as a hash
                    client.hset(f"h3:{h3_cell}", mapping=value)

        aggregated_data.printSchema()

        query = (
            aggregated_data.writeStream.outputMode("update")
            .foreachBatch(write_to_redis)
            .option("checkpointLocation", "/tmp/spark-checkpoints")
            .start()
        )

        return query
