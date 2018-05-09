#
# Module imports
import os
from recording.src.recording.config_interface import ConfigInterface
from recording.src.recording.recording_interface import RecordingInterface
from recording.src.recording.text_interface import TextInterface
from recording.src.constants import path_consts as pc
from recording.src.producer.producer import Producer, ProducerHandler
from recording.src.coding_framework.BDAConfigParser import g_config
"""
This script is intended to run on producer nodes. The
producer node will be responsible for capturing and
submission of data onto the Kafka Broker.
"""
#
# Script Parameters
stream_offset = os.environ.get(g_config.get_value('ProducerRunner', 'StreamOffset_EvnVarName'))
if stream_offset is not None:
    stream_offset = int(stream_offset)
    print('Stream offset extracted from env variable % d' % stream_offset)
else:
    stream_offset = int(g_config.get_value('ProducerRunner', 'stream_offset'))
    print('Stream offset extracted from config file % d' % stream_offset)
#
# Connection strings used to connect to a number of Kafka Brokers
kafka_connection_strings = os.environ.get('kafka_connection_strings')
if kafka_connection_strings is not None:
    kafka_connection_strings = kafka_connection_strings.split(',')
    print('Kafka connection strings, extracted from env variable: %s' % kafka_connection_strings)
else:
    kafka_connection_strings = g_config.get_value('ProducerRunner', 'kafka_connection_strings').split(',')
    print('Kafka connection strings, extracted from config file: %s' % kafka_connection_strings)
file_segment_time_span = int(g_config.get_value('ProducerRunner', 'file_segment_time_span'))            # File recording segment size (seconds)
file_extension = g_config.get_value('ProducerRunner', 'file_extension')                                 # File recording extension to save the file (Set to flac for Google Storage purposes)
file_quality = g_config.get_value('ProducerRunner', 'file_quality')                                     # Video quality to record stream at
kafka_topic_video = g_config.get_value('ProducerRunner', 'kafka_topic_video')                                       # Kafka topic which this produces will subscribe to
kafka_topic_text = g_config.get_value('ProducerRunner', 'kafka_topic_text')
exception_time_out = g_config.get_value('ProducerRunner', 'exception_time_out')                         # Time in seconds to delay process in the case of a timeout
youtube_api_result_limit = g_config.get_value('ProducerRunner', 'youtube_api_result_limit')
#
print("Initiating producer runner..")
#
# Loads config from input_channels.json
ci = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
#
if ci.get_input_channels()[stream_offset].type == kafka_topic_video:
    interface = RecordingInterface(config_obj=ci.get_input_channels()[stream_offset],
                                   segment_time_span=file_segment_time_span,
                                   extension=file_extension,
                                   quality=file_quality,
                                   video_buffer_path=pc.DIR_VIDEO_BUFFER)
elif ci.get_input_channels()[stream_offset].type == kafka_topic_text:
    interface = TextInterface(ci.get_input_channels()[stream_offset])
else:
    raise("Unsupported source type - Must be 'video' or 'text'")
#
# Creating an instance of the producer logic, and connecting with brokers
producer = Producer()
producer.connect(kafka_connection_strings)
#
# Loads config object
config_obj = ci.get_input_channels()[stream_offset]
#
# Video Livestreaming
if config_obj.get_src_type() == 0:
    # Initiates streamlink, to record footage locally of ongoing livestream
    while True:
        #
        # Initiates a call to Streamlink, and records the stream into a file locally
        video_path = interface.capture_and_return()
        #
        # video = ri.get_video(video_path=video_path)
        ProducerHandler.produce_message(data=video_path,
                                        kafka_producer=producer,
                                        kafka_config=config_obj.get_details(),
                                        kafka_topic=kafka_topic_video)
#
# Video Retrieval (YouTube Specific)
elif config_obj.get_src_type() == 1:
    # Initiates a call to a local video file, and splits it into several files
    video_paths = interface.download_and_segment()
    #
    for video_path in video_paths:
        ProducerHandler.produce_message(data=video_path,
                                        kafka_producer=producer,
                                        kafka_config=config_obj.get_details(),
                                        kafka_topic=kafka_topic_video)
#
elif config_obj.get_src_type() == 2:
    raise("Not Yet Supported!")
#
# Text Retrieval (YouTube Comments Section Specific)
elif config_obj.get_src_type() == 3:
    # Initiates a call to YouTube page, and retrieves all comments and comment threads using YouTube api
    comments = interface.get_youtube_comments(youtube_api_result_limit=youtube_api_result_limit)
    for author, comment in comments.items():
        ProducerHandler.produce_message(data=[author,comment],
                                        kafka_producer=producer,
                                        kafka_config=config_obj.get_details(),
                                        kafka_topic=kafka_topic_text)
