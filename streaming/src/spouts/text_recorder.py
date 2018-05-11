#
# Module Imports
from streamparse import Spout
from coding_framework.BDAConfigParser import g_config
from kafka.consumer import Consumer # Module purposely starting from kafka.consum...
import json
import os
#
class TextRecorder(Spout):
    """
    Storm Spout Logic

    Responsible for offloading streaming objects containing
    text data (both real-time and prerecorded).
    """
    #
    # Grouping Mechanism
    outputs = ['text']
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
            kafka_connection_strings = g_config.get_value('ConsumerRunner', 'kafka_connection_strings').split(',')
            print('Kafka connection strings, extracted from config file: %s' % kafka_connection_strings)

        # Connection string used to connect to Zookeeper
        zookeeper_connection = os.environ.get('zookeeper_connection')
        if zookeeper_connection is not None:
            print('ZooKeeper connection string, extracted from env variable: %s' % zookeeper_connection)
        else:
            zookeeper_connection = g_config.get_value('ConsumerRunner', 'zookeeper_connection')
            print('ZooKeeper connection string, extracted from config file: %s' % zookeeper_connection)

        kafka_topic = "text"  # Kafka topic which this produces will subscribe to
        kafka_consumer_group = "testgroup"  # Kafka consumer group name for balanced consumers
        #
        self.log("Initiating Text KafkaSpout..")
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
        self.log("Balanced Consumer (Text) Established.")
    #
    def next_tuple(self):
        """
        Submitter method for Spout, emits captured
        and segmented text down the pipeline
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
            #stream_obj = message.replace("'", "\"")
            #self.log(message)
            stream_obj = json.loads(message)
        except ImportError as e:
            self.log(str(e))
            return
        except Exception as e:
            self.log(str(e) + " Viewer [" + str(stream_obj['viewer']) + "] ,Text [" + str(stream_obj['text']) + "]")
            return
        #
        # Stream_obj (which is now represented as a dictionary)
        # is pushed down stream through Storm, towards awaiting
        # text_decoder bolts
        if not stream_obj:
            return
        #
        self.emit([json.dumps(stream_obj)])
        self.log("Object de-pickled and pushed downstream - " + str(stream_obj['viewer']))