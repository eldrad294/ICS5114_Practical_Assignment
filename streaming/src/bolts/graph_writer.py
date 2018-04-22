#
# Module Imports
from streamparse import Bolt
from graph.CRUD_interface import CRUDInterface
from coding_framework.BDAConfigParser import g_config
#
class GraphWriter(Bolt):
    """
    This bolt contains the logic required to
    interface with the graph database storage.

    The bolt is paired to read from a video_decoder
    bolt, receive the text and transform/insert this
    information into a graph.
    """
    #
    # Grouping Mechanism
    outputs = ['video']
    #
    def initialize(self, conf, ctx):
        """
        GraphWriter initialize method
        :param conf:
        :param ctx:
        :return:
        """
        uri = g_config.get_value('GraphDB', 'neo4j_connection_string')
        user = g_config.get_value('GraphDB', 'user')
        password = g_config.get_value('GraphDB', 'password')
        self.interface = CRUDInterface(uri=uri,
                                       user=user,
                                       password=password)
    #
    def process(self, tup):
        """
        Receives strings of text and writes them to
        the graph database in the form of nodes/relationships
        :param tup:
        :return:
        """
        streaming_object = tup.values[0]
        #
        self.log("Entry 5")
        if not streaming_object or not streaming_object['video_text']:
            return
        self.log("Entry 5")
        #
        word_list = streaming_object['video_text']
        streamer = streaming_object['channel']
        genre = streaming_object['genre']
        platform = streaming_object['platform']
        #
        self.log("Entry 6")
        for word in word_list:
            #
            # streamer - [utters] - word
            self.interface.merge_relationship("streamer", streamer,
                                              "word", word,
                                              "utters")
            #
            # genre - [features] - word
            for g in list(genre):
                self.interface.merge_relationship("genre", g,
                                                  "word", word,
                                                  "features")
            #
            # Increment word count
            self.interface.increment_node("word", word)
        #
        # streamer - [partakes] - genre
        for g in list(genre):
            self.interface.merge_relationship("streamer", streamer,
                                              "genre", g,
                                              "partakes")
        #
        # streamer - [uses] - platform
        self.interface.merge_relationship("streamer", streamer,
                                          "platform", platform,
                                          "uses")