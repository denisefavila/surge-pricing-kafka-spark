from kafka.admin import KafkaAdminClient, NewTopic


def create_kafka_topic(
    topic_name, num_partitions, replication_factor, bootstrap_servers
):

    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers, api_version=(2.4)
    )
    topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )

    admin_client.create_topics([topic])

    admin_client.close()

    print(
        f"Topic {topic_name} created with {num_partitions} partitions and replication factor {replication_factor}"
    )
