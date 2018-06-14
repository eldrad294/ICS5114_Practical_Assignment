#
# Module Imports
from graph.basic_interface import BasicInterface
from graph.transaction_functions import UpdateTransactionFunctions
#
class UpdateInterface(BasicInterface):
    """
    A class focused on the update aspect of the Neo4J Implementation
    """
    def __init__(self, uri, user, password):
        BasicInterface.__init__(self, uri, user, password)
    #
    def increment_node(self, node_type, node_name):
        """
        Updates graph edge by 1
        :param node_type:
        :param node_name:
        :return:
        """
        node_type = node_type.lower()
        node_name = node_name.lower()
        #
        if node_type not in self.supported_node_types:
            print("Unsupported node type - ["+str(node_type)+"]")
            return None
        #
        with self._driver.session() as session:
            if node_type == self.supported_node_types[3]:
                session.write_transaction(UpdateTransactionFunctions.increment_word_node, node_name)
                print("'Word' node incremented")