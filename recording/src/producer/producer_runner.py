#
# Module imports
from recording.src.recording.config_interface import ConfigInterface
from recording.src.recording.recording_interface import RecordingInterface
from recording.src.recording.text_interface import TextInterface
from recording.src.constants import path_consts as pc
from recording.src.producer.producer import Producer, ProducerHandler
from recording.src.coding_framework.BDAConfigParser import g_config
import os
#
"""
This script is intended to run on producer nodes. The producer node will be responsible for capturing and submission of
data onto the Kafka Broker.
"""
class ProducerRunner:
    ###################
    # Private members
    __stream_offset = None
    __kafka_connection_strings = None
    __file_segment_time_span = None         # File recording segment size (seconds)
    __file_extension = None                 # File recording storage extension (GoogleStorage recommends FLAC)
    __file_quality = None                   # Recorded stream video quality
    __kafka_topic_video = None              # Kafka topic which this producer will subscribe to
    __kafka_topic_text = None
    __exception_time_out = None             # Time in seconds to delay process in the case of a timeout
    __youtube_api_result_limit = None
    __recording_iface = None
    __recording_config_container = None
    __producer = None
    __producer_handler = None
    ###################

    def __init__(self):
        self.__load_producer_params()
        self.__initialize_producer()

    def start_producer(self):
        print('>> ProducerRunner --> Start')
        if self.__recording_config_container.get_src_type() == 0:
            # Video live streaming
            self.__video_live_streaming()
        elif self.__recording_config_container.get_src_type() == 1:
            # Video Retrieval (YouTube Specific)
            self.__video_retrieval_youtube()
        elif self.__recording_config_container.get_src_type() == 2:
            # Text Retrieval (Twitch.Tv) live chat extraction
            self.__text_retrieval_twitch()
        elif self.__recording_config_container.get_src_type() == 3:
            # Text Retrieval (YouTube Comments Section Specific)
            self.__text_retrieval_youtube()
        else:
            raise ValueError('Invalid source type')

    def __load_producer_params(self):
        print('>> ProducerRunner --> Load config')
        self.__stream_offset = int(self.__load_param('ProducerRunner', 'stream_offset', 'StreamOffset_EvnVarName'))
        self.__kafka_connection_strings = self.__load_param('ProducerRunner', 'kafka_connection_strings',
                                                            'KafkaConnectionStrings_EvnVarName').split(',')
        self.__file_segment_time_span = int(self.__load_param('ProducerRunner', 'file_segment_time_span'))
        self.__file_extension = self.__load_param('ProducerRunner', 'file_extension')
        self.__file_quality = self.__load_param('ProducerRunner', 'file_quality')
        self.__kafka_topic_video = self.__load_param('ProducerRunner', 'kafka_topic_video')
        self.__kafka_topic_text = self.__load_param('ProducerRunner', 'kafka_topic_text')
        self.__exception_time_out = self.__load_param('ProducerRunner', 'exception_time_out')
        self.__youtube_api_result_limit = self.__load_param('ProducerRunner', 'youtube_api_result_limit')
        print('<< ProducerRunner --> Load config')

    def __load_param(self, section_name: str, key_name: str, key_env_var: str=None) -> str:
        """
        Helper method, responsible for loading ProducerRunner config parameter
        :param section_name:  Section name within the config.ini file
        :param key_name:      Parameter key within the config.ini file
        :param key_env_var:   If set, load parameter from the environment variable or from config.ini file, in this
                              order.
        :return:              String representation of the config param
        """
        result = None

        if key_env_var:
            result = os.environ.get(g_config.get_value(section_name, key_env_var))

        if result is None:
            result = g_config.get_value(section_name, key_name)

        return result

    def __initialize_producer(self):
        print('>> ProducerRunner --> Initialization')
        # Loads config from input_channels.json
        config_iface = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
        #
        if config_iface.get_input_channels()[self.__stream_offset].type == self.__kafka_topic_video:
            self.__recording_iface = RecordingInterface(
                config_obj=config_iface.get_input_channels()[self.__stream_offset],
                segment_time_span=self.__file_segment_time_span,
                extension=self.__file_extension,
                quality=self.__file_quality,
                video_buffer_path=pc.DIR_VIDEO_BUFFER)
        elif config_iface.get_input_channels()[self.__stream_offset].type == self.__kafka_topic_text:
            self.__recording_iface = TextInterface(config_iface.get_input_channels()[self.__stream_offset])
        else:
            raise ValueError("Unsupported source type - Must be 'video' or 'text'")

        # Loads config object
        self.__recording_config_container = config_iface.get_input_channels()[self.__stream_offset]

        # Creating an instance of the producer logic and connecting with brokers
        self.__producer = Producer()
        self.__producer.connect(self.__kafka_connection_strings)

        upload_thread_count = int(self.__load_param('ProducerRunner', 'UploadThreadCount'))
        self.__producer_handler = ProducerHandler(self.__producer, upload_thread_count)
        print('<< ProducerRunner --> Initialization')

    def __video_live_streaming(self):
        # Initiates streamlink, record ongoing live-stream footage locally
        print('>> ProducerRunner --> Video live streaming')
        while True:
            # Initiates a call to Streamlink, and records the stream into a file locally
            video_path = self.__recording_iface.capture_and_return()

            if video_path is not None:
                self.__producer_handler.add_task(data=video_path,
                                                 kafka_config=self.__recording_config_container.get_details(),
                                                 kafka_topic=self.__kafka_topic_video)
            else:
                print('__video_live_streaming --> capture_and_return() returned None')

    def __video_retrieval_youtube(self):
        # Initiates a call to a local video file and splits it into several files
        print('>> ProducerRunner --> YouTube video live streaming')
        video_paths = self.__recording_iface.download_and_segment()

        for video_path in video_paths:
            if video_path is not None:
                self.__producer_handler.add_task(data=video_path,
                                                 kafka_config=self.__recording_config_container.get_details(),
                                                 kafka_topic=self.__kafka_topic_video)
            else:
                print('__video_retrieval_youtube --> download_and_segment() returned None')
        print('<< ProducerRunner --> YouTube video live streaming')

    def __text_retrieval_youtube(self):
        """
        Initiates a call to YouTube page, and retrieves all comments and comment threads using YouTube api

        :return:
        """
        print('>> ProducerRunner --> YouTube text retrieval')
        comments = self.__recording_iface.get_youtube_comments(youtube_api_result_limit=self.__youtube_api_result_limit)
        for author, comment in comments.items():
            self.__producer_handler.add_task(data=[author, comment],
                                             kafka_config=self.__recording_config_container.get_details(),
                                             kafka_topic=self.__kafka_topic_text)
        print('<< ProducerRunner --> YouTube text retrieval')

    def __text_retrieval_twitch(self):
        """
        Initiates IRC connection to Twitch TV streaming channel.
        Call is blocking, and will only return upon termination
        of the producer.

        :return:
        """
        print('>> ProducerRunner --> Twitch.Tv text retrieval')
        self.__recording_iface.start_twitch_bot(producer_handler=self.__producer_handler,
                                                kafka_config=self.__recording_config_container.get_details(),
                                                kafka_topic=self.__kafka_topic_text)
        print('<< ProducerRunner --> Twitch.TV text retrieval')
#
producer_runner = ProducerRunner()
producer_runner.start_producer()
