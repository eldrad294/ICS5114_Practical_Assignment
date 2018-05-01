#
# Module Imports
from pykafka.exceptions import ConsumerStoppedException
from streamparse import Spout
from kafka.consumer import Consumer # Module purposely starting from kafka.consum...
import pickle
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
        kafka_topic = "video"  # Kafka topic which this produces will subscribe to
        kafka_consumer_group = "testgroup"  # Kafka consumer group name for balanced consumers
        #
        self.log("Initiating KafkaSpout..")
        #
        # Creating an instance of the consumer logic, and connecting with brokers
        consumer = Consumer()
        consumer.connect(kafka_connection_strings)
        #
        # Establishing balanced consumer connection.
        self.bconsumer = consumer.set_balanced_consumer(topic=kafka_topic,
                                                        consumer_group=kafka_consumer_group,
                                                        zookeeper_connect=zookeeper_connection,
                                                        auto_commit_enable=True,
                                                        reset_offset_on_start=True)
        self.log("Balanced Consumer Established.")
        #
        # Establishing simple consumer connection.
        #self.sconsumer = consumer.set_simple_consumer(topic=kafka_topic)
    #
    def next_tuple(self):
        """
        Submitter method for Spout, emits captured
        and segmented video file paths
        :return:
        """
        #
        # Consumes message from Kafka Broker. 'block'
        # parameter must be set to false or otherwise
        # will hog Storm Spout and get timed out
        message = self.bconsumer.consume(block=False)
        if not message:
            # nothing to emit
            return
        self.log("Message offloaded from consumer..")
        #
        try:
            #
            # De-serializes kafka message value
            stream_obj = pickle.loads(message.value)
            self.log("Object de-pickled and pushed downstream - " + str(stream_obj['file_path']))
        except ImportError as e:
            self.log(str(e))
            return
        except Exception as e:
            self.log(str(e))
            return
        #
        # Stream_obj (which is now represented as a dictionary)
        # is pushed down stream through Storm, towards awaiting
        # video_decoder bolts
        if not stream_obj:
            return
        self.emit([stream_obj])