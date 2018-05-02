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
        self.log("GRAPH LOG(1)")
        streaming_object = tup.values[0]
        #
        self.log("GRAPH LOG(2)")
        if not streaming_object or not streaming_object['video_text']:
            self.log("GRAPH LOG(3)")
            return
        #
        self.log("GRAPH LOG(4)")
        self.log("Preparing batch for graph writing..")
        #
        word_list = streaming_object['video_text']
        streamer = streaming_object['channel']
        genre = streaming_object['genre']
        platform = streaming_object['platform']
        #
        self.log("GRAPH LOG(5)")
        try:
            #
            # Creates streamer node
            self.log("GRAPH LOG(6)")
            self.interface.merge_node("streamer", streamer)
            #
            # Creates platform node
            self.log("GRAPH LOG(7)")
            self.interface.merge_node("platform", platform)
            #
            for g in list(genre):
                #
                # Creates genre node
                self.interface.merge_node("genre", g)
            self.log("GRAPH LOG(8)")
            #
            for word in word_list:
                #
                # Creates word node
                self.log("GRAPH LOG(9)" + word)
                self.interface.merge_node("word",word)
                #
                # streamer - [utters] - word
                self.interface.merge_relationship("streamer", streamer,
                                                  "word", word,
                                                  "utters")
                #
                # genre - [features] - word
                for g in list(genre):
                    #
                    # word - [features] - genre
                    self.log("GRAPH LOG(10)")
                    self.interface.merge_relationship("genre", g,
                                                      "word", word,
                                                      "features")
                self.log("GRAPH LOG(11)")
            #
            # streamer - [partakes] - genre
            for g in list(genre):
                self.interface.merge_relationship("streamer", streamer,
                                                  "genre", g,
                                                  "partakes")
            self.log("GRAPH LOG(12)")
            #
            # streamer - [uses] - platform
            self.interface.merge_relationship("streamer", streamer,
                                              "platform", platform,
                                              "uses")
            #
            self.log("Batch written to graph..")
        except Exception as e:
            self.log("An exception was raised during graph writing!!")
            self.log(str(e))