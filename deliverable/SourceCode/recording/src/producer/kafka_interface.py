class KafkaInterface(object):
    """
    Defines the kafka producer/consumer interface
    """
    def __init__(self):
        pass

    def connect(self, address):
        """
        Method which defines connecting information
        :param address:  Kafka connection string
        :return:
        """
        raise NotImplementedError

    def connect_ssl(self, address, cafile, certfile, keyfile, password):
        """
        Method which uses and SSL connection to Kafka broker
        :param address:  Kafka connection string
        :param cafile:   CA certificate file
        :param certfile: Client certificate
        :param keyfile:  Client private key
        :param password: Password for private key
        :return:         None
        """
        raise NotImplementedError

    def list_topics(self):
        """
        Returns a list of topics from the Kafka Broker
        :return:         None
        """
        raise NotImplementedError

    def get_topic(self, topic):
        """
        Gets a particular topic from Kafka broker and returns an encoded version of the topic
        :param topic:    Kafka topic
        :return:         None
        """
        raise NotImplementedError
