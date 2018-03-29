#
# Module Imports
from pykafka import KafkaClient, SslConfig
from src.kafka.kafka_interface import KafkaInterface
#
class Consumer(KafkaInterface):
    """
    Class encapsulating consumer functionality
    """
    #
    def __init__(self):
        KafkaInterface.__init__(self)
        self.client = None
    #
    def connect(self, address, ssl_config=None):
        """
        Attempts to connect to Kafka brokers
        :param address:
        :return:
        """
        # Formats connection string in the form of 127.0.0.1:9092,127.0.0.1:9090,...
        connection_string = ","
        connection_string = connection_string.join(address)
        try:
            print("Consumer attempting to connect to Kafka brokers at " + connection_string + " ...")
            if ssl_config is None:
                self.client = KafkaClient(hosts=connection_string)
            else:
                self.client = KafkaClient(hosts=connection_string,
                                          ssl_config=ssl_config)
            print("Consumer connected to Kafka broker at these addresses ["+connection_string+"]")
        except Exception as e:
            print(str(e))
    #
    def connect_ssl(self, address, cafile, certfile, keyfile, password):
        """
        Uses an SSL connection to connect to Kafka Broker
        :param address:
        :param cafile:
        :param certfile:
        :param keyfile:
        :param password:
        :return:
        """
        config = SslConfig(cafile=cafile,
                           certfile=certfile,
                           keyfile=keyfile,
                           password=password)
        #
        self.connect(address=address,
                     ssl_config=config)
    #
    def list_topics(self):
        """
        Gets list of topics from Kafka broker.
        WARNING: This method is likely to be incompatible
        with python 3.x
        :return:
        """
        return self.client.topics
    #
    def get_topic(self, topic):
        """
        Gets a particular topic from Kafka broker, and
        returns an encoded version of the topic
        :param topic:
        :return:
        """
        # topic string is converted to bytes to appease Kafka
        return self.client.topics[topic.encode('utf-8')]
    #
    def simple_consumer(self, topic):
        """
        Consumes messages from defined topic, and prints them
        :param topic:
        :return:
        """
        #
        consumer = None
        try:
            consumer = self.get_topic(topic).get_simple_consumer()
        except Exception as e:
            print("An error occurred whilst attempting retrieval from broker!")
            print(str(e))
        #
        for message in consumer:
            if message is not None:
                print(message.offset, message.value)
    #
    def balanced_consumer(self, topic, consumer_group, zookeeper_connect, auto_commit_enable=False):
        """
        Consumes messages from defined topic, and prints them.
        Uses the balanced consumer method for safe multi-topic
        consumption
        :param topic:
        :return:
        """
        #
        consumer = None
        try:
            consumer = self.get_topic(topic).get_balanced_consumer(consumer_group=consumer_group.encode('utf-8'),
                                                                   auto_commit_enable=auto_commit_enable,
                                                                   zookeeper_connect=zookeeper_connect)
        except Exception as e:
            print("An error occurred whilst attempting retrieval from broker!")
            print(str(e))
        #
        for message in consumer:
            if message is not None:
                print(message.offset, message.value)
