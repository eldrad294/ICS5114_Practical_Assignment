#
# Module Imports
from graph.basic_interface import BasicInterface
from graph.transaction_functions import DeleteTransactionFunctions
#
class DeleteInterface(BasicInterface):
    """
    A class focused on the delete aspect of the Neo4J Implementation
    """
    def __init__(self, uri, user, password):
        BasicInterface.__init__(self, uri, user, password)
    #
    def delete_node(self, node_type_1, node_value_1):
        """
        Deletes a single node and any adjoining relations
        :param node_type_1:
        :param node_value_1:
        :param node_type_2:
        :param node_value_2:
        :param relationship:
        :return:
        """
        #
        node_type_1 = node_type_1.lower()
        node_value_1 = node_value_1.lower()
        if node_type_1 not in self.supported_node_types:
            print("Unsupported node type - [" + str(node_type_1) + "]")
            return False
        #
        with self._driver.session() as session:
            session.write_transaction(DeleteTransactionFunctions.delete_relationship,
                                      node_value_1,
                                      node_type_1)
            print("'" + node_type_1 + "' node deleted")
        #
        # If we got this far, this means that node creation was successful
        return True
    #
    def delete_relationship(self, node_type_1, node_value_1, node_type_2=None, node_value_2=None, relationship=None):
        """
        Deletes a single relationship in the graph structure
        :param node_type_1:
        :param node_name_1:
        :param node_type_2:
        :param node_name_2:
        :param relationship:
        :return:
        """
        node_type_1 = node_type_1.lower()
        node_value_1 = node_value_1.lower()
        if node_type_1 not in self.supported_node_types:
            print("Unsupported node type - [" + str(node_type_1) + "]")
            return False
        #
        if node_type_2 is not None:
            node_type_2 = node_type_2.lower()
            node_value_2 = node_value_2.lower()
            if node_type_2 not in self.supported_node_types:
                print("Unsupported node type - [" + str(node_type_2) + "]")
                return False
        #
        relationship = relationship.lower()
        if relationship not in self.supported_relationship_types:
            print("Unsupported relationship type - [" + str(relationship) + "]")
            return False
        #
        with self._driver.session() as session:
            session.write_transaction(DeleteTransactionFunctions.delete_relationship,
                                      node_value_1,
                                      node_value_2,
                                      node_type_1,
                                      node_type_2,
                                      relationship)
            print("'" + relationship + "' relationship deleted")
        #
        # If we got this far, this means that node creation was successful
        return True