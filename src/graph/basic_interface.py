#
# Module Imports
from neo4j.v1 import GraphDatabase
from graph.graph_entities import GraphEntities
#
class BasicInterface(object):
    """
    Interface class which serves as the base for all Neo4j interface inherited classes.
    """
    #
    def __init__(self, uri, user, password):
        """
        Interface Constructor, which attempts to connect to Graph instance
        :param host:
        :param user:
        :param password:
        """
        #
        self._driver = None
        self.supported_node_types = GraphEntities.get_supported_node_types()
        self.supported_relationship_types = GraphEntities.get_supported_relationship_types()
        try:
            #
            # Attempts to establish connection with Graph database
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print(str(e))
            #
        #
    #
    def close(self):
        """
        Closes graph database connection
        :return:
        """
        self._driver.close()
