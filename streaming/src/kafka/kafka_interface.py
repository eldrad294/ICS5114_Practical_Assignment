class KafkaInterface(object):
    """
    Defines the kafka producer/consumer interface
    """
    def __init__(self):
        pass

    def connect(self, address):
        """
        Method which defines connecting information
        :param address:
        :return:
        """
        raise NotImplementedError

    def connect_ssl(self, address, cafile, certfile, keyfile, password):
        """
        Method which uses and SSL connection to Kafka broker
        :param cafile:
        :param certfile:
        :param keyfile:
        :param password:
        :return:
        """
        raise NotImplementedError

    def list_topics(self):
        """
        Returns a list of topics from the Kafka Broker
        :return:
        """
        raise NotImplementedError

    def get_topic(self, topic):
        """
        Gets a particular topic from Kafka broker, and
        returns an encoded version of the topic
        :param topic:
        :return:
        """
        raise NotImplementedError
