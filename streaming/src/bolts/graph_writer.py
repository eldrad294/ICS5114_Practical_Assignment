#
# Module Imports
from streamparse import Bolt
from graph.CRUD_interface import CRUDInterface
from coding_framework.BDAConfigParser import g_config
import json
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
    outputs = ['video','text']
    #
    # Overriding Bolt Configuration
    auto_anchor = True
    auto_ack = True
    auto_fail = False
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
        #streaming_object = streaming_object.replace("'", "\"")
        streaming_object = json.loads(streaming_object)
        # self.log(streaming_object)
        #
        if not streaming_object or not streaming_object['text']:
            return
        #
        self.log("Preparing batch for graph writing..")
        #
        viewer = streaming_object['viewer']
        word_list = streaming_object['text']
        self.log(word_list)
        streamer = str(streaming_object['channel'])
        genre = streaming_object['genre']
        platform = str(streaming_object['platform'])
        #
        try:
            self.log("GRAPHWRITER1")
            #
            # Creates streamer node
            self.interface.merge_node("streamer", streamer)
            self.log("GRAPHWRITER2")
            #
            # Creates platform node
            self.interface.merge_node("platform", platform)
            #
            #self.log("Viewer [" + viewer + "]")
            if viewer is not None:
                self.log("GRAPHWRITER3")
                #
                # Creates viewer node
                self.interface.merge_node("viewer", viewer)
            #
            for g in list(genre):
                self.log("GRAPHWRITER4 [" + g + "]")
                #
                # Creates genre node
                self.interface.merge_node("genre", g)
                self.log("GRAPHWRITER4.5 [" + g + "]")
            #
            for word in word_list:
                self.log("GRAPHWRITER5")
                #
                # Creates word node
                self.interface.merge_node("word", word)
                if viewer is None:
                    #
                    # streamer - [utters] - word
                    self.interface.merge_relationship("streamer", streamer,
                                                      "word", word,
                                                      "utters")
                    self.log("GRAPHWRITER6.5 Word[" + word + "] Streamer[" + streamer + "]")
                else:
                    self.log("GRAPHWRITER6")
                    #
                    # viewer - [comments] - word
                    self.interface.merge_relationship("viewer", viewer,
                                                      "word", word,
                                                      "comments")
                    self.log("GRAPHWRITER6.5 Word[" + word + "] Viewer[" + viewer + "]")
            for g in list(genre):
                self.log("GRAPHWRITER7")
                #
                # streamer - [partakes] - genre
                self.interface.merge_relationship("streamer", streamer,
                                                  "genre", g,
                                                  "partakes")
                if viewer is not None:
                    self.log("GRAPHWRITER8 Viewer[" + viewer + "] Genre[" + g + "]")
                    #
                    # viewer - [follows] - genre
                    self.interface.merge_relationship("viewer", viewer,
                                                      "genre", g,
                                                      "follows")
                    self.log("GRAPHWRITER8.5 Viewer[" + viewer + "] Genre[" + g + "]")
            self.log("GRAPHWRITER9")
            #
            # streamer - [uses] - platform
            self.interface.merge_relationship("streamer", streamer,
                                              "platform", platform,
                                              "uses")
            if viewer is not None:
                self.log("GRAPHWRITER10 Viewer[" + viewer + "] Streamer[" + streamer + "]")
                #
                # viewer - [subscribes] - streamer
                self.interface.merge_relationship("viewer", viewer,
                                                  "streamer", streamer,
                                                  "subscribes")
                self.log("GRAPHWRITER11 Viewer[" + viewer + "] Streamer[" + streamer + "]")
            #
            self.log("Batch written to graph..")
        except Exception as e:
            self.log("An exception was raised during graph writing!!")
            self.log(str(e))