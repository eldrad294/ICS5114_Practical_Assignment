# --------------------------------
# Video Capture Tool - How TO
# --------------------------------
from src.recording.config_interface import ConfigInterface
from src.recording.recording_interface import RecordingInterface
from src.constants import path_consts as pc
#
# Loads config from input_channels.json
ci = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
#
# Records video streams to disk locally
ri = RecordingInterface(config_obj=ci.get_input_channels()[0],
                        segment_time_span=30,
                        extension="wav",
                        quality="worst")
video = ri.get_video(ri.capture_and_return())
# --------------------------------
# Kafka Producer - How TO
# --------------------------------
from src.kafka.producer import Producer
from src.kafka.consumer import Consumer
connection_string=["127.0.0.1:9092"]
p1 = Producer()
p1.connect(connection_string)
#print(p1.list_topics())
p1.produce_message(topic='video', stream_object=video)
#
c1 = Consumer()
c1.connect(connection_string)
#print(c1.list_topics())
c1.simple_consumer(topic='video')
# c1.balanced_consumer(topic='video',
#                      consumer_group='testgroup',
#                      zookeeper_connect="localhost:2181",
#                      auto_commit_enable=True)