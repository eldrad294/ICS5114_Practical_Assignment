#
# Module Imports
from graph.basic_interface import BasicInterface
from graph.transaction_functions import CreateTransactionFunctions
#
class CreateInterface(BasicInterface):
    """
    A class focused on the create aspect of the Neo4J Implementation
    """
    def __init__(self, uri, user, password):
        BasicInterface.__init__(self, uri, user, password)
    #
    def merge_node(self, node_type, node_name):
        """
        This function oversees creation of nodes. It ensures that
        only nodes of the following types are created:

        * streamer
        * viewer
        * genre
        * word

        The function also ensures to avoid duplicated creation
        of nodes by utilizing the MERGE keyword.

        :param node_type:
        :param name:
        :return:
        """
        #
        node_type = node_type.lower()
        node_name = node_name.lower()
        bookmark = None
        #
        if node_type not in self.supported_node_types:
            return bookmark
        #
        with self._driver.session() as session:
            return 'ThisIsATest'
            if node_type == self.supported_node_types[0]:
                session.write_transaction(CreateTransactionFunctions.add_streamer, node_name)
            elif node_type == self.supported_node_types[1]:
                session.write_transaction(CreateTransactionFunctions.add_viewer, node_name)
            elif node_type == self.supported_node_types[2]:
                session.write_transaction(CreateTransactionFunctions.add_genre, node_name)
            elif node_type == self.supported_node_types[3]:
                session.write_transaction(CreateTransactionFunctions.add_word, node_name)
            elif node_type == self.supported_node_types[4]:
                session.write_transaction(CreateTransactionFunctions.add_platform, node_name)
            else:
                return bookmark
            #
            bookmark = session.last_bookmark()
        #
        # If we got this far, this means that node creation was successful
        return bookmark
    #
    def merge_relationship(self, node_type_1, node_name_1, node_type_2, node_name_2, relationship):
        #
        #saved_bookmarks = [] # To collect session bookmarks (causal chaining)
        node_type_1 = node_type_1.lower()
        node_name_1 = node_name_1.lower()
        node_type_2 = node_type_2.lower()
        node_name_2 = node_name_2.lower()
        relationship = relationship.lower()
        #
        if node_type_1 not in self.supported_node_types:
            return False
        #
        if node_type_2 not in self.supported_node_types:
            return False
        #
        if relationship not in self.supported_relationship_types:
            return False
        #
        # Merging node 1
        #bookmark = self.merge_node(node_type=node_type_1,
        #                           node_name=node_name_1)
        #saved_bookmarks.append(bookmark)
        #
        # Merging node 2
        #bookmark = self.merge_node(node_type=node_type_2,
        #                           node_name=node_name_2)
        #saved_bookmarks.append(bookmark)
        #
        """
        Bookmarks are used to ensure that previous transactions were successfully
        carried out, before commencing the next transaction.
        
        Causal chaining has been disabled, since bookmarks are not being typecasted
        successfully - Library Bug:
        
            raise ValueError("Invalid bookmark: {}".format(b0))
            ValueError: Invalid bookmark: neo4j:bookmark:v1:tx32
        """
        #with self._driver.session(bookmarks=saved_bookmarks) as session:
        with self._driver.session() as session:
            if relationship == self.supported_relationship_types[0]:
                session.write_transaction(CreateTransactionFunctions.add_uterrance, node_name_1, node_name_2)
            elif relationship == self.supported_relationship_types[1]:
                session.write_transaction(CreateTransactionFunctions.add_comment, node_name_1, node_name_2)
            elif relationship == self.supported_relationship_types[2]:
                session.write_transaction(CreateTransactionFunctions.add_features, node_name_1, node_name_2)
            elif relationship == self.supported_relationship_types[3]:
                session.write_transaction(CreateTransactionFunctions.add_follows, node_name_1, node_name_2)
            elif relationship == self.supported_relationship_types[4]:
                session.write_transaction(CreateTransactionFunctions.add_partakes, node_name_1, node_name_2)
            elif relationship == self.supported_relationship_types[5]:
                session.write_transaction(CreateTransactionFunctions.add_subscribes, node_name_1, node_name_2)
            elif relationship == self.supported_relationship_types[6]:
                session.write_transaction(CreateTransactionFunctions.add_uses, node_name_1, node_name_2)
            else:
                return False
        #
        # If we got this far, this means that node creation was successful
        return True