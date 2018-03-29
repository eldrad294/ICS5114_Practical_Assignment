#
# Module Imports
from pykafka import KafkaClient, SslConfig
from src.kafka.kafka_interface import KafkaInterface
import pickle
#
class Producer(KafkaInterface):
    """
    Class encapsulating producer functionality
    """
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
            print("Producer attempting to connect to Kafka brokers at " + connection_string + " ...")
            if ssl_config is None:
                self.client = KafkaClient(hosts=connection_string)
            else:
                self.client = KafkaClient(hosts=connection_string,
                                          ssl_config=ssl_config)
            print("Producer connected to Kafka broker at these addresses ["+connection_string+"]")
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
        return self.client.topics[topic.encode()] #topic string is converted to bytes to appease Kafka
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
        with self.get_topic(topic).get_sync_producer() as producer:
            #
            # Pushes serialized object onto Kafka broker
            producer.produce(serialized_stream_object)
            print("stream_object submitted to broker!")


