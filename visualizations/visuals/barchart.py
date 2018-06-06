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
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
    #
    def draw_word_per_streamer(self, save_path):
        """
        Plots a bar graph of all streamers, and respective word count

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
        # Plot visualization from cursor
        streamers, variety_count, tot_count = [], [], []
        for rec in cursor:
            streamers.append(rec['streamer'])
            variety_count.append(rec['variety_count'])
            tot_count.append(rec['tot_count'])
        data = Data([
            Bar(
                x=streamers,
                y=variety_count,
                name='Unique Vocab'
            ),
            Bar(x=streamers,
                y=tot_count,
                name='Total Words')
            ])
        layout = go.Layout(
            barmode='group',
            title="Streamer Word Variety Distribution"
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_word_per_platform(self, save_path):
        """
        Plots a bar graph of all platforms, and respective word count

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_word_per_platform)
        #
        # Plot visualization from cursor
        platforms, variety_count, tot_count = [], [], []
        for rec in cursor:
            platforms.append(rec['platform'])
            variety_count.append(rec['variety_count'])
            tot_count.append(rec['tot_count'])
        data = Data([
            Bar(
                x=platforms,
                y=variety_count,
                name='Unique Vocab'
            ),
            Bar(x=platforms,
                y=tot_count,
                name='Total Words')
            ])
        layout = go.Layout(
            barmode='group',
            title="Platform Word Variety Distribution"
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_word_per_viewer(self, save_path):
        """
        Plots a bar graph of all viewers, and respective word count

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_word_per_viewer)
        #
        # Plot visualization from cursor
        viewers, variety_count, tot_count = [], [], []
        for rec in cursor:
            viewers.append(rec['viewer'])
            variety_count.append(rec['variety_count'])
            tot_count.append(rec['tot_count'])
        data = Data([
            Bar(
                x=viewers,
                y=variety_count,
                name='Unique Vocab'
            ),
            Bar(x=viewers,
                y=tot_count,
                name='Total Words')
        ])
        layout = go.Layout(
            barmode='group',
            title="Viewer Word Variety Distribution"
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_word_per_genre(self, save_path):
        """
        Plots a bar graph of all genres, and respective word count

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_word_per_genre)
        #
        # Plot visualization from cursor
        genre, variety_count, tot_count = [], [], []
        for rec in cursor:
            genre.append(rec['genre'])
            variety_count.append(rec['variety_count'])
            tot_count.append(rec['tot_count'])
        data = Data([
            Bar(
                x=genre,
                y=variety_count,
                name='Unique Vocab'
            ),
            Bar(x=genre,
                y=tot_count,
                name='Total Words')
        ])
        layout = go.Layout(
            barmode='group',
            title="Genre Word Variety Distribution"
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_top_foul_streamers(self, save_path):
        """
        Plots a bar graph of top 20 streamers, ranked by highest occurrence of foul word usage

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_top_foul_streamers)
        #
        # Plot visualization from cursor
        streamer, count = [], []
        for rec in cursor:
            streamer.append(rec['streamer'])
            count.append(rec['tot_foul'])
        data = Data([
            Bar(
                x=streamer,
                y=count,
                name='Foul Word Count'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Top Foul Worded Streamers",
            xaxis=dict(title="Streamers"),
            yaxis=dict(title="Foul Word Count")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_top_foul_viewers(self, save_path):
        """
        Plots a bar graph of top 20 viewers, ranked by highest occurrence of foul word usage

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_top_foul_viewers)
        #
        # Plot visualization from cursor
        viewer, count = [], []
        for rec in cursor:
            viewer.append(rec['viewer'])
            count.append(rec['tot_foul'])
        data = Data([
            Bar(
                x=viewer,
                y=count,
                name='Foul Word Count'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Top Foul Worded Viewers",
            xaxis=dict(title="Viewers"),
            yaxis=dict(title="Foul Word Count")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_top_foul_platforms(self, save_path):
        """
        Plots a bar graph of top 20 platforms, ranked by highest occurrence of foul word usage

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_top_foul_platforms)
        #
        platform = {}
        for rec in cursor:
            if rec['platform'] in platform:
                platform[rec['platform']] += rec['tot_foul']
            else:
                platform[rec['platform']] = rec['tot_foul']
        #
        platforms, count = [], []
        for key,value in platform.items():
            platforms.append(key)
            count.append(value)
        #
        data = Data([
            Bar(
                x=platforms,
                y=count,
                name='Foul Word Count'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Top Foul Worded Platforms",
            xaxis=dict(title="Platforms"),
            yaxis=dict(title="Foul Word Count")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
        #
        # Close connection to graph db
        gi.close()
    #
    def draw_top_foul_genre(self, save_path):
        """
        Plots a bar graph of top 20 genres, ranked by highest occurrence of foul word usage

        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_top_foul_genre)
        #
        platform = {}
        for rec in cursor:
            if rec['genre'] in platform:
                platform[rec['genre']] += rec['tot_foul']
            else:
                platform[rec['genre']] = rec['tot_foul']
        #
        platforms, count = [], []
        for key, value in platform.items():
            platforms.append(key)
            count.append(value)
        #
        data = Data([
            Bar(
                x=platforms,
                y=count,
                name='Foul Word Count'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Top Foul Worded Genre",
            xaxis=dict(title="Genres"),
            yaxis=dict(title="Foul Word Count")
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
        return tx.run(Cypher.cypher_word_per_streamer())
    #
    @staticmethod
    def load_word_per_platform(tx):
        return tx.run(Cypher.cypher_word_per_platform())
    #
    @staticmethod
    def load_word_per_viewer(tx):
        return tx.run(Cypher.cypher_word_per_viewer())
    #
    @staticmethod
    def load_word_per_genre(tx):
        return tx.run(Cypher.cypher_word_per_genre())
    #
    @staticmethod
    def load_top_foul_streamers(tx):
        return tx.run(Cypher.cypher_foul_word_streamer())
    #
    @staticmethod
    def load_top_foul_viewers(tx):
        return tx.run(Cypher.cypher_foul_word_viewer())
    #
    @staticmethod
    def load_top_foul_platforms(tx):
        return tx.run(Cypher.cypher_foul_word_platform())
    #
    @staticmethod
    def load_top_foul_genre(tx):
        return tx.run(Cypher.cypher_foul_word_genre())