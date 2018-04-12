#
# Module imports
from recording.src.recording.config_interface import ConfigInterface
from recording.src.recording.recording_interface import RecordingInterface
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
stream_offset = int(g_config.get_value('ProducerRunner', 'stream_offset'))
file_segment_time_span = int(g_config.get_value('ProducerRunner', 'file_segment_time_span'))            # File recording segment size (seconds)
file_extension = g_config.get_value('ProducerRunner', 'file_extension')                                 # File recording extension to save the file (Set to flac for Google Storage purposes)
file_quality = g_config.get_value('ProducerRunner', 'file_quality')                                     # Video quality to record stream at
kafka_connection_strings = g_config.get_value('ProducerRunner', 'kafka_connection_strings').split(",")  # Connection strings used to connect to a number of Kafka Brokers
kafka_topic = g_config.get_value('ProducerRunner', 'kafka_topic')                                       # Kafka topic which this produces will subscribe to
exception_time_out = g_config.get_value('ProducerRunner', 'exception_time_out')                         # Time in seconds to delay process in the case of a timeout
#
print("Initiating producer runner..")
#
# Loads config from input_channels.json
ci = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
#
# Records video streams to disk locally
ri = RecordingInterface(config_obj=ci.get_input_channels()[stream_offset],
                        segment_time_span=file_segment_time_span,
                        extension=file_extension,
                        quality=file_quality,
                        video_buffer_path=pc.DIR_VIDEO_BUFFER)
#
# Creating an instance of the producer logic, and connecting with brokers
producer = Producer()
producer.connect(kafka_connection_strings)
#
# Loads config object
config_obj = ci.get_input_channels()[stream_offset].get_details()
#
# Producer Loop
while True:
    #
    # Initiates a call to Streamlink, and records the stream into a file locally
    video_path = ri.capture_and_return()
    #
    # video = ri.get_video(video_path=video_path)
    ProducerHandler.produce_message(video_path, producer, config_obj, kafka_topic)
#
# Testing Loop
# from src.kafka.stream_object import StreamObject
# import time
# while True:
#     #
#     # Initiates a call to Streamparse, and records the stream into a file locally
#     video_path = ri.capture_and_return()
#     #
#     # video = ri.get_video(video_path=video_path)
#     # Prepares the message to be submitted over to Kafka, by creating an object of type stream_object
#     stream_object = StreamObject(platform=config_obj['platform'],
#                                  src_url=config_obj['url'],
#                                  channel=config_obj['channel'],
#                                  genre=config_obj['genre'],
#                                  time_stamp=time.ctime(),
#                                  file_path=video_path,
#                                  cloud_bucket_name="Test",
#                                  cloud_bucket_path="Test",
#                                  file=None)
#
#     # Submits message to Kafka broker
#     producer.produce_message(topic=kafka_topic, stream_object=stream_object)