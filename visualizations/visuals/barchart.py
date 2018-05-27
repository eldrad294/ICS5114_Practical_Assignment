from visualizations.utils.graph_connector import GraphInterface
from visualizations.utils.cypher import Cypher
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
#
class BarChart():
    """
    Loads data from Neo4j
    and formats it into
    a barchart visualization
    """
    def draw_word_per_streamer(self, uri, user, password, save_path):
        """
        Plots a bar graph of all streamers, and respective word count

        :param uri:         Graph DB uri
        :param user:        Graph DB User
        :param password:    Graph DB Password
        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=uri, user=user, password=password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_word_per_streamer)
        #
        # Plot visualization from cursor
        streamers, count = [], []
        for rec in cursor:
            streamers.append(rec['streamer'])
            count.append(rec['count'])
        data = Data([
            Bar(
                x=streamers,
                y=count
            )
        ])
        layout = go.Layout(
            title="Streamer Word Distribution"
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
#
class Transactions():
    @staticmethod
    def load_word_per_streamer(tx):
        return tx.run(Cypher.cypher_words_per_streamer())