from utils.graph_connector import GraphInterface
from utils.cypher import Cypher
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#
class WordCloudChart():
    """
    Loads data from Neo4j
    and formats it into
    a word cloud visualization
    """
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
    #
    def draw_ratio_wordcloud(self, save_path):
        """
        Plots a word graph based off Neo4j words

        :param uri:         Graph DB uri
        :param user:        Graph DB User
        :param password:    Graph DB Password
        :param save_path:   Path where to save html plot
        :return:
        """
        #
        # Establishes connection to graph database
        gi = GraphInterface(uri=self.uri, user=self.user, password=self.password)
        #
        # Establish session and return cursor
        with gi.get_driver().session() as session:
            cursor = session.read_transaction(Transactions.load_word_graph)
        #
        words = []
        [words.append(rec['word']) for rec in cursor]
        #
        wordcloud = WordCloud(
            background_color='white',
            #stopwords=stopwords,
            #max_words=200,
            max_font_size=40,
            scale=3,
            random_state=1  # chosen at random by flipping a coin; it was heads
        ).generate(str(words))

        fig = plt.figure(1, figsize=(12, 12))
        plt.axis('off')
        # if title:
        #     fig.suptitle(title, fontsize=20)
        #     fig.subplots_adjust(top=2.3)
        plt.imshow(wordcloud)
        #plt.show()
        fig.savefig(save_path)
    #
class Transactions():
    @staticmethod
    def load_word_graph(tx):
        return tx.run(Cypher.cypher_word_cloud())