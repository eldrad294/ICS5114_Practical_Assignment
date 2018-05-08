#
# Module Imports
from pykafka.exceptions import ConsumerStoppedException
from streamparse import Spout
from src.coding_framework.BDAConfigParser import g_config
from kafka.consumer import Consumer # Module purposely starting from kafka.consum...
import json
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
        # Connection strings used to connect to a number of Kafka Brokers
        kafka_connection_strings = os.environ.get('kafka_connection_strings')
        if kafka_connection_strings is not None:
            kafka_connection_strings = kafka_connection_strings.split(',')
            print('Kafka connection strings, extracted from env variable: %s' % kafka_connection_strings)
        else:
            kafka_connection_strings = g_config.get_value('ProducerRunner', 'kafka_connection_strings').split(',')
            print('Kafka connection strings, extracted from config file: %s' % kafka_connection_strings)

        # Connection string used to connect to Zookeeper
        zookeeper_connection = os.environ.get('zookeeper_connection')
        if zookeeper_connection is not None:
            print('ZooKeeper connection string, extracted from env variable: %s' % zookeeper_connection)
        else:
            zookeeper_connection = g_config.get_value('ConsumerRunner', 'zookeeper_connection')
            print('ZooKeeper connection string, extracted from config file: %s' % zookeeper_connection)

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
            message = message.value.decode()
            stream_obj = message.replace("'", "\"")
            stream_obj = json.loads(stream_obj)
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
        #
        self.emit([json.dumps(stream_obj)])
