from utils.graph_connector import GraphInterface
from utils.cypher import Cypher
from plotly.offline import plot
from plotly.graph_objs import *
import plotly.graph_objs as go
import json
import webbrowser, os
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
    def draw_tree_graph(self, save_path, html_path, viewer=None):
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
            cursor = session.read_transaction(Transactions.load_word_per_viewer,viewer)
        #
        viewer, duplicate_viewer, comment_count, word, foul_flag = [], [], [], [], []
        for rec in cursor:
            viewer.append(rec['viewer'])
            comment_count.append(rec['comment_count'])
            word.append(rec['word'])
            foul_flag.append(rec['foul_flag'])
        #
        json_nodes_string = '{"nodes":['
        json_edges_string = '],"links":['
        #
        for i in range(len(word)):
            if viewer[i] not in duplicate_viewer:
                json_nodes_string += '{"id":"' + str(viewer[i]) + '","group":1},'
                duplicate_viewer.append(viewer[i])
            if foul_flag[i] != 'false':
                json_nodes_string += '{"id":"' + str(word[i]) + '" ,"group":2}'
            else:
                if comment_count[i] < 5:
                    json_nodes_string += '{"id":"' + str(word[i]) + '" ,"group":3}'
                elif comment_count[i] > 6 and comment_count[i] < 10:
                    json_nodes_string += '{"id":"' + str(word[i]) + '" ,"group":4}'
                else:
                    json_nodes_string += '{"id":"' + str(word[i]) + '" ,"group":5}'
            json_edges_string += '{"source":"' + str(word[i]) + '","target":"' + str(viewer[i]) + '", "value":"' + str(comment_count[i]) + '"}'
            if i != len(word)-1:
                json_nodes_string += ','
                json_edges_string += ','
        json_string = json_nodes_string + json_edges_string + "]}"
        #
        # Write JSON string to file
        with open(save_path,'w', encoding='utf-8') as outfile:
            json.dump(json.JSONDecoder().decode(json_string), outfile)
        #
        # Open HTML file which feeds upon the above created JSON file
        webbrowser.open('file://' + os.path.realpath(html_path))
#
class Transactions():
    @staticmethod
    def load_word_per_viewer(tx, viewer):
        return tx.run(Cypher.cypher_viewer_word_relationship(viewer))