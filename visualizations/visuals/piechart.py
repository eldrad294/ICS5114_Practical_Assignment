from visualizations.utils.graph_connector import GraphInterface
from visualizations.utils.cypher import Cypher
from plotly.offline import plot
import plotly.graph_objs as go
#
class PieChart():
    """
    Loads data from Neo4j
    and formats it into
    a piechart visualization
    """
    #
    def draw_ratio_piechart(self, uri, user, password, save_path):
        """
        Plots a pie chart based off Neo4j word distribution

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
            cursor = session.read_transaction(Transactions.load_ratio_graph)
        #
        # Plot visualization from cursor
        labels, count = [],[]
        for rec in cursor:
            labels.append(rec['label'])
            count.append(rec['count'])
        trace = go.Pie(labels=labels, values=count)
        data = [trace]
        layout = go.Layout(
            title="Node Distribution"
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
    def load_ratio_graph(tx):
        return tx.run(Cypher.cypher_ratio_piechart())