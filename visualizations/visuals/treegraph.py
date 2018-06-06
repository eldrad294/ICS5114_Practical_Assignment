from visualizations.utils.graph_connector import GraphInterface
from visualizations.utils.cypher import Cypher
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
#
class TreeGraph():
    """
    Loads data from Neo4j
    and formats it into
    a graph visualization
    """
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
    #
    def draw_tree_graph(self, save_path):
        """
        Plots a tree graph visualization of a particular viewer, with all word relationships

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_word_per_streamer)
        #
        """
        Following chunk needs to re-written, to process:
        http://graphalchemist.github.io/Alchemy/#/examples
        """
        # viewer, comment_count, word, foul_flag = [], [], [], []
        # for rec in cursor:
        #     viewer.append(rec['viewer'])
        #     comment_count.append(rec['comment_count'])
        #     word.append(rec['word'])
        #     foul_flag.append(rec['foul_flag'])
        # #
        # json_string = '{"nodes":['
        # for i in range(len(word)):

#
class Transactions():
    @staticmethod
    def load_word_per_streamer(tx):
        return tx.run(Cypher.cypher_viewer_word_relationship())