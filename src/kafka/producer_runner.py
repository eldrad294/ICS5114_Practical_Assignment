#
# Module imports
from src.recording.config_interface import ConfigInterface
from src.recording.recording_interface import RecordingInterface
from src.constants import path_consts as pc
from src.kafka.producer import Producer
from src.object_definitions.stream_object import StreamObject
from src.speech_recognition.BDAGoogleStorage import BDAGoogleStorageConvertUpload
import time
"""
This script is intended to run on producer nodes. The
producer node will be responsible for capturing and
submission of data onto the Kafka Broker.
"""
#
# Script Parameters
stream_offset = 0
file_segment_time_span = 30                 # File recording segment size
file_extension = "wav"                      # File recording extension to save the file
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
ri = RecordingInterface(config_obj=ci.get_input_channels()[0],
                        segment_time_span=file_segment_time_span,
                        extension=file_extension,
                        quality=file_quality,
                        video_buffer_path=pc.DIR_VIDEO_BUFFER)
#
# Creating an instance of the producer logic, and connecting with brokers
producer = Producer()
producer.connect(kafka_connection_strings)
#
while True:
    try:
        #
        # Initiates a call to Streamparse, and records the stream into a file locally
        video_path = ri.capture_and_return()
        #
        # Copies the recorded file into memory, as a collection of binary data
        # video = ri.get_video(video_path=video_path)

        cloud_url_tuple = None

        # NOTE: - This is a synchronous call. Execution will be held until operation
        #         is complete.
        #       - BDAGoogleStorageConvertUpload may raise a ValueError exception
        gs_convert_upload = BDAGoogleStorageConvertUpload(video_path)
        # cloud_url_tuple[0] --> BucketName
        # cloud_url_tuple[1] --> BlobPath
        cloud_url_tuple = gs_convert_upload.upload_file()

        # [Nik]: - Consider deleting the video file at this point? --> os.remove(video_path)

        # Prepares the message to be submitted over to Kafka, by creating an object of type stream_object
        config_obj = ci.get_input_channels()[stream_offset].get_details()
        stream_object = StreamObject(platform=config_obj['platform'],
                                     src_url=config_obj['url'],
                                     channel=config_obj['channel'],
                                     genre=config_obj['genre'],
                                     time_stamp=time.ctime(),
                                     file_path=video_path,
                                     cloud_url=cloud_url_tuple,
                                     file=None)
        #
        # Submits message to Kafka broker
        producer.produce_message(topic=kafka_topic, stream_object=stream_object)
    except Exception as e:
        print(str(e))
        # In the case of an exception arising in video capture, handling, Kafka Submission,
        # we put the main thread to sleep for n seconds, to avoid resource exhaustion.
        time.sleep(exception_time_out)