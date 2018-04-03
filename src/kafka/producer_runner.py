#
# Module imports
from src.recording.config_interface import ConfigInterface
from src.recording.recording_interface import RecordingInterface
from src.constants import path_consts as pc
from src.kafka.producer import Producer, ProducerHandler

"""
This script is intended to run on producer nodes. The
producer node will be responsible for capturing and
submission of data onto the Kafka Broker.
"""

# [Nik]: - Consider pushing such parameters in the config.ini file?
# Script Parameters
stream_offset = 2
file_segment_time_span = 30                 # File recording segment size (seconds)
file_extension = "flac"                     # File recording extension to save the file (Set ot flac for Google Storage purposes)
file_quality = "worst"                      # Video quality to record stream at
kafka_connection_strings=["127.0.0.1:9092"] # Connection strings used to connect to a number of Kafka Brokers
kafka_topic = 'video'                       # Kafka topic which this produces will subscribe to
exception_time_out = 10                     # Time in seconds to delay process in the case of a timeout
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
while True:
    #
    # Initiates a call to Streamparse, and records the stream into a file locally
    video_path = ri.capture_and_return()
    #
    # video = ri.get_video(video_path=video_path)
    ProducerHandler.produce_message(video_path, producer, config_obj, kafka_topic)

    # [Nik]: - What is the execution frequency of this loop? - Denoted by video_segment_size
    #        - Consider throttling this loop? (given stream_offset is never modified)- Any throttling results in delay/downtime of stream recording. Not recommended.
