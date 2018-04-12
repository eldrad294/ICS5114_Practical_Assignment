#
# Neo4J Main

# # --------------------------------
# # Video Capture Tool - How TO
# # --------------------------------
# from src.recording.config_interface import ConfigInterface
# from src.recording.recording_interface import RecordingInterface
# from src.constants import path_consts as pc
# #
# # Loads config from input_channels.json
# ci = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
# #
# # Records video streams to disk locally
# ri = RecordingInterface(config_obj=ci.get_input_channels()[0],
#                         segment_time_span=30,
#                         extension="wav",
#                         quality="worst")
# video = ri.get_video(ri.capture_and_return())
# # --------------------------------
# # Kafka Producer - How TO
# # --------------------------------
# from src.kafka.producer import Producer
# from src.kafka.consumer import Consumer
# connection_string=["127.0.0.1:9092"]
# p1 = Producer()
# p1.connect(connection_string)
# #print(p1.list_topics())
# p1.produce_message(topic='video', stream_object=video)
# #
# c1 = Consumer()
# c1.connect(connection_string)
# #print(c1.list_topics())
# c1.simple_consumer(topic='video')
# # c1.balanced_consumer(topic='video',
# #                      consumer_group='testgroup',
# #                      zookeeper_connect="localhost:2181",
# #                      auto_commit_enable=True)

from src.graph.CRUD_interface import CRUDInterface
uri = "bolt://localhost:7687"
user = "neo4j"
password = "lol123"
interface = CRUDInterface(uri=uri,
                            user=user,
                            password=password)
#
# output = interface.merge_node("word","hello")
# print(output)
#
output = interface.merge_relationship("streamer",
                                      "raphael",
                                      "word",
                                      "bye",
                                      "utters")

output = interface.delete_relationship(node_type_1="streamer",
                                       node_value_1="raphael",
                                       node_type_2="word",
                                       node_value_2="bye",
                                       relationship="utters")
print(output)