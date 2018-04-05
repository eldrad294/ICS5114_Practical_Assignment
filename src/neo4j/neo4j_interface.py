#
# Module Imports
from neo4j.v1 import GraphDatabase
#
class Neo4jInterface:
    """
    Interface class through which all Graph database transactions are handled.
    """
    #
    def __init__(self,host,user,password):
        """
        Interface Constructor, which attempts to connect to Graph instance
        :param host:
        :param user:
        :param password:
        """
        #
        self.__driver = None
        try:
            #
            # Attempts to establish connection with Graph database
            self.__driver = GraphDatabase.driver(host, auth=(user, password))
        except Exception as e:
            print(str(e))
        #
    #
    def close(self):
        """
        Closes graph database connection
        :return:
        """
        self.__driver.close()