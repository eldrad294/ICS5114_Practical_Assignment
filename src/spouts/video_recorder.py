#
# Module Imports
from pykafka.exceptions import ConsumerStoppedException
from streamparse import Spout
from kafka.consumer import Consumer
import pickle
import time
#
class VideoRecorder(Spout):
    """
    Storm Spout Logic

    Responsible for offloading data off streaming websites,
    and emits data as a series of segmented videos down
    the topology pipeline.
    """
    #
    # Grouping Mechanism
    outputs = ['video']
    #
    def initialize(self, stormconf, context):
        """
        Storm Spout 'constructor method'
        :param storm_conf:
        :param context:
        :return:
        """
        #
        # Script Parameters
        kafka_connection_strings = ["127.0.0.1:9092"]  # Connection strings used to connect to a number of Kafka Brokers
        zookeeper_connection = "127.0.0.1:2181"  # Connection string used to connect to Zookeeper
        kafka_topic = "video"  # Kafka topic which this produces will subsribe to
        kafka_consumer_group = "testgroup"  # Kafka consumer group name for balanced consumers
        #
        print("Initiating KafkaSpout..")
        self.log("Initiating KafkaSpout..");
        #
        # Creating an instance of the consumer logic, and connecting with brokers
        consumer = Consumer()
        consumer.connect(kafka_connection_strings)
        #
        # Establishing consumer connection
        self.bconsumer = consumer.set_balanced_consumer(topic=kafka_topic,
                                                        consumer_group=kafka_consumer_group,
                                                        zookeeper_connect=zookeeper_connection,
                                                        auto_commit_enable=True)
    #
    def next_tuple(self):
        """
        Submitter method for Spout, emits captured
        and segmented video file paths
        :return:
        """
        try:
            #
            # Consumes message from Kafka Broker
            message = self.bconsumer.consume()
            #
            # De-serializes kafka message value
            stream_obj = pickle.loads(message.value)
            self.emit([stream_obj])
        except ConsumerStoppedException:
            self.bconsumer.stop()
            self.log("Restarting stopped pykafka consumer..")
            self.bconsumer.start()
        except ImportError:
            pass
        except Exception as e:
            self.log(str(e))
