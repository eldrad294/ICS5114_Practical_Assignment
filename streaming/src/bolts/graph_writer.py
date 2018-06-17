import json
import os
from streamparse import Bolt
from graph.CRUD_interface import CRUDInterface
from coding_framework.BDAConfigParser import g_config


class GraphWriter(Bolt):
    """
    This bolt contains the logic required to interface with the graph database storage.
    The bolt is paired to read from a video_decoder bolt, receive the text and transform/insert this information into a
    graph.
    """
    # Grouping Mechanism
    outputs = ['video', 'text']

    # Overriding Bolt Configuration
    auto_anchor = True
    auto_ack = True
    auto_fail = False

    def initialize(self, conf, ctx):
        """
        GraphWriter initialize method
        :param conf: Unused param
        :param ctx:  Unused param
        :return:     None
        """
        uri = os.environ.get('neo4j_connection_string')
        if uri is None:
            uri = g_config.get_value('GraphDB', 'neo4j_connection_string')
            
        user = g_config.get_value('GraphDB', 'user')
        password = g_config.get_value('GraphDB', 'password')
        self.interface = CRUDInterface(uri=uri, user=user, password=password)

    def process(self, tup):
        """
        Receives strings of text and writes them to the graph database in the form of nodes/relationships
        :param tup:
        :return:
        """
        streaming_object = tup.values[0]
        streaming_object = json.loads(streaming_object)

        if not streaming_object or not streaming_object['text']:
            return

        self.log("Preparing batch for graph writing..")

        viewer = streaming_object['viewer']
        word_list = list(streaming_object['text'])
        streamer = str(streaming_object['channel'])
        genre = list(streaming_object['genre'])
        platform = str(streaming_object['platform'])

        try:
            # Creates streamer node
            self.interface.merge_node("streamer", streamer)

            # Creates platform node
            self.interface.merge_node("platform", platform)

            if viewer is not None:
                # Creates viewer node
                self.interface.merge_node("viewer", viewer)

            for word in word_list:
                # Creates word node
                self.interface.merge_node("word", word)
                if viewer is None:
                    # streamer - [utters] - word
                    self.interface.merge_relationship("streamer", streamer, "word", word, "utters")
                else:
                    # viewer - [comments] - word
                    self.interface.merge_relationship("viewer", viewer, "word", word, "comments")
            for g in genre:
                # Creates genre node
                self.interface.merge_node("genre", g)

                # streamer - [partakes] - genre
                self.interface.merge_relationship("streamer", streamer, "genre", g, "partakes")
                if viewer is not None:
                    # viewer - [follows] - genre
                    self.interface.merge_relationship("viewer", viewer, "genre", g, "follows")

            # streamer - [uses] - platform
            self.interface.merge_relationship("streamer", streamer, "platform", platform, "uses")
            if viewer is not None:
                # viewer - [subscribes] - streamer
                self.interface.merge_relationship("viewer", viewer, "streamer", streamer, "subscribes")

            self.log("Batch written to graph..")
        except Exception as e:
            self.log("An exception was raised during graph writing!!")
            self.log(str(e))
