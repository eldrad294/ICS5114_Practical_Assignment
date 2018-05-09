#
# Module Imports
from pykafka import KafkaClient, SslConfig
from recording.src.producer.kafka_interface import KafkaInterface
from recording.src.speech_recognition.BDAGoogleStorage import BDAGoogleStorageConvertUpload
from recording.src.producer.stream_object import StreamObject
import os
import time
import threading
import json
#
class Producer(KafkaInterface):
    ###################
    # Private members
    __threadLock = None
    ###################
    """
    Class encapsulating producer functionality
    """
    def __init__(self):
        KafkaInterface.__init__(self)
        self.client = None
        self.__threadLock = threading.Lock()
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
        Pushes a stream_object onto a Kafka broker, as defined by the topic.
        Operation is thread safe.
        :param topic:
        :param stream_object:
        :return:
        """
        #
        # Serializes stream object
        self.__threadLock.acquire()
        try:
            #
            # Object is serialized as a dictionary
            string_stream_object = json.dumps(stream_object.get_details())
            serialized_stream_object = string_stream_object.encode('utf-8')
            with self.get_topic(topic).get_sync_producer() as producer:
                #
                # Pushes serialized object onto Kafka broker
                producer.produce(serialized_stream_object)
                print("stream_object submitted to Kafka broker with topic [" + str(topic) + "]..")
        finally:
            self.__threadLock.release()


class ProducerHandler:
    @staticmethod
    def produce_message(data, kafka_producer, kafka_config, kafka_topic):
        """
        ProducerHandler entry point:
        1. Initiates a separate thread.
        2. Delegates work to the thread. No thread management is done.
        :param data:           Absolute path to video file or list made of [authors, comments]
        :param kafka_producer: Kafka producer
        :param kafka_config:   Kafka configuration
        :param kafka_topic:    Kafka topic
        :return:               None
        """
        if kafka_topic == "video":
            print(data)
            thread_fire_forget = threading.Thread(target=ProducerHandler.__process_file,
                                                  args=(data,
                                                        kafka_producer,
                                                        kafka_config,
                                                        kafka_topic))
            thread_fire_forget.start()
        elif kafka_topic == "text":
            ProducerHandler.__process_file(data=data,
                                           kafka_producer=kafka_producer,
                                           kafka_config=kafka_config,
                                           kafka_topic=kafka_topic)
        else:
            raise ("Unsupported Kafka Topic! Aborting..")



    @staticmethod
    def __process_file(data, kafka_producer, kafka_config, kafka_topic):
        """
        1. Converts the input video file into FLAC audio format (48000Hz, 1-channel).
        2. Uploads resulting file to Google Storage.
        3. Posts the resulting task to Kafka.
        :param data:           Absolute path to video file OR [author, comment]
        :param kafka_producer: Kafka producer
        :param kafka_config:   Kafka configuration
        :param kafka_topic:    Kafka topic
        :return:               None
        """
        if kafka_topic == "video":
            cloud_url_tuple = ProducerHandler.__convert_upload(data)
            ProducerHandler.__post_kafka(data=data,
                                         kafka_producer=kafka_producer,
                                         kafka_config=kafka_config,
                                         kafka_topic=kafka_topic,
                                         cloud_url_tuple=cloud_url_tuple)
            #print(video_path)
            os.remove(data) # Remove segmented file from disk
        elif kafka_topic == "text":
            ProducerHandler.__post_kafka(data=data,
                                         kafka_producer=kafka_producer,
                                         kafka_config=kafka_config,
                                         kafka_topic=kafka_topic,
                                         cloud_url_tuple=None)
        else:
            raise ("Unsupported Kafka Topic! Aborting..")

    @staticmethod
    def __convert_upload(data):
        """
        Convert media file to FLAC and upload to Google Storage platform.
        :param data: Absolute path to video file
        :return:           (BucketName, BlobPath)
        """
        gs_convert_upload = BDAGoogleStorageConvertUpload(data)
        return gs_convert_upload.upload_file()

    @staticmethod
    def __post_kafka(data, kafka_producer, kafka_config, kafka_topic, cloud_url_tuple):
        """
        1. Construct the Kafka message.
        2. Post message through the thread-safe method: Producer::produce_message(..)
        :param data:            Absolute path to video file OR extracted text [author, comment]
        :param kafka_producer:  Kafka producer
        :param kafka_config:    Kafka configuration
        :param kafka_topic:     Kafka topic
        :param cloud_url_tuple: Google Storage URI
        :return:                None
        """
        # Prepares the message to be submitted over to Kafka, by creating an object of type stream_object
        if kafka_topic == "video":
            stream_object = StreamObject(platform=kafka_config['platform'],
                                         src_url=kafka_config['src'],
                                         channel=kafka_config['channel'],
                                         genre=kafka_config['genre'],
                                         time_stamp=time.ctime(),
                                         file_path=data,
                                         cloud_bucket_name=cloud_url_tuple[0],
                                         cloud_bucket_path=cloud_url_tuple[1],
                                         text=None)
        elif kafka_topic == "text":
            stream_object = StreamObject(platform=kafka_config['platform'],
                                         src_url=kafka_config['src'],
                                         channel=kafka_config['channel'],
                                         genre=kafka_config['genre'],
                                         time_stamp=time.ctime(),
                                         file_path=None,
                                         cloud_bucket_name=None,
                                         cloud_bucket_path=None,
                                         text=data)
        else:
            raise ("Unsupported Kafka Topic! Aborting..")
        #
        # Submits message to Kafka broker
        kafka_producer.produce_message(topic=kafka_topic, stream_object=stream_object)
