#
# Module Imports
from pykafka import KafkaClient
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
    def connect(self, address):
        """
        Attempts to connect to Kafka broker
        :param address:
        :return:
        """
        try:
            print("Attempting to connect to Kafka broker at " + address + " ...")
            self.client = KafkaClient(hosts=address)
            print("Connected to Kafka broker at this address ["+address+"]")
        except Exception as e:
            print(str(e))
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
        return self.client.topics[topic.encode('utf-8')] #topic string is converted to bytes to appease Kafka
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
    def balanced_consumer(self, topic):
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
            consumer = self.get_topic(topic).get_balanced_consumer(consumer_group='testgroup')
        except Exception as e:
            print("An error occurred whilst attempting retrieval from broker!")
            print(str(e))
        #
        for message in consumer:
            if message is not None:
                print(message.offset, message.value)
