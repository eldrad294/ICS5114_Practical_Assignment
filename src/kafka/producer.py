#
# Module Imports
from pykafka import KafkaClient
import pickle
#
class Producer:
    """
    Class encapsulating producer functionality
    """
    def __init__(self):
        self.client = None
    #
    def connect_producer(self, address):
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
        Gets list of topics from Kafka broker
        :return:
        """
        return self.client.topics
    #
    def get_topic(self, topic):
        """
        Gets a particular topic from Kafka broker
        :param topic:
        :return:
        """
        return self.client.topics[topic]
    #
    def produce_message(self, topic, stream_object):
        """
        Pushes a stream_object onto a Kafka broker, as defined by the topic
        :param topic:
        :param stream_object:
        :return:
        """
        #
        # Serializes stream object
        serialized_stream_object = pickle.dumps(stream_object)
        with self.get_topic(topic).sync_producer() as producer:
            #
            # Pushes serialized object onto Kafka broker
            producer.produce(serialized_stream_object)


