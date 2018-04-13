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

from streaming.src.graph.CRUD_interface import CRUDInterface
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
word_list = ['look', "'s", 'hardly', '48', 'hours', 'much', 'still', 'unknown', 'things', 'say', 'certain', 'actually', 'helps', 'HBO', 'things', 'saved', 'without', 'restraint', 'many', 'necessary', 'appropriate', 'moments', 'Silence', 'moment', 'premium', 'cable', 'profanity', 'things', 'stand', 'first', 'know', 'attack', 'carried', 'gigantic', 'fucking', 'assholes', 'unconscionable', 'flaming', 'ass', 'holes', 'possibly', 'possibly', 'working', 'fucking', 'All', 'Souls', 'definitely', 'working', 'service', 'open', 'Audiology', 'second', 'I', "'m", 'saying', 'French', 'going', 'enjoy', 'I', "'ll", 'tell', 'war', 'culture', 'lifestyle', 'frogs', 'good', 'fucking', 'luck', 'bring', 'bankruptcy', 'geology', 'bring', 'Jean-Paul', 'Sartre', 'fine', 'wine', 'go', 'buy', 'cigarettes', 'Camembert', 'macarons', 'proof', 'fucking', 'croquembouche', 'trust', 'pulled', 'philosophy', 'rigorous', 'self-abnegation', 'pastry', 'fight', 'friends', 'fuc', 'French', 'Freedom', 'Tower', 'tell', 'people', 'France', 'thoughts', 'truly', 'I', 'doubt', "'ll", 'say', 'events', 'spool', 'going', 'continue']
streamer = "John Oliver"
genre = ["News","Entertainment"]
platform = "YouTube"
#
for word in word_list:
    #
    # streamer - [utters] - word
    interface.merge_relationship("streamer", streamer,
                                      "word", word,
                                      "utters")
    #
    # genre - [features] - word
    for g in list(genre):
        interface.merge_relationship("genre", g,
                                          "word", word,
                                          "features")
    #
    # Increment word count
    interface.increment_node("word", word)
#
# streamer - [partakes] - genre
for g in list(genre):
    interface.merge_relationship("streamer", streamer,
                                      "genre", g,
                                      "partakes")
#
# streamer - [uses] - platform
interface.merge_relationship("streamer", streamer,
                                  "platform", platform,
                                  "uses")