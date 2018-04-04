#
# Module imports
from src.kafka.consumer import Consumer
from src.coding_framework.BDAConfigParser import g_config
"""
This script is intended to run on consumer nodes. The
consumer node will be responsible for polling the Kafka
broker, and redirecting stream_objects down the pipeline,
effectively into the Storm Topology
"""
#
# Script Parameters
kafka_connection_strings = g_config.get_value('ConsumerRunner', 'kafka_connection_strings').split(",") # Connection strings used to connect to a number of Kafka Brokers
zookeeper_connection = g_config.get_value('ConsumerRunner', 'zookeeper_connection')                    # Connection string used to connect to Zookeeper
kafka_topic = g_config.get_value('ConsumerRunner', 'video')                                            # Kafka topic which this produces will subsribe to
kafka_consumer_group = g_config.get_value('ConsumerRunner', 'kafka_consumer_group')                    # Kafka consumer group name for balanced consumers
#
print("Initiating consumer runner..")
#
# Creating an instance of the producer logic, and connecting with brokers
consumer = Consumer()
consumer.connect(kafka_connection_strings)
#
bconsumer = consumer.set_balanced_consumer(topic=kafka_topic,
                                           consumer_group=kafka_consumer_group,
                                           zookeeper_connect=zookeeper_connection,
                                           auto_commit_enable=True)
#
if bconsumer is not None:
    for message in bconsumer:
        if message is not None:
            print(message.offset)
            print(type(message.value))
else:
    print("Balanced consumer was not setup!..Exiting!")
    exit(1)