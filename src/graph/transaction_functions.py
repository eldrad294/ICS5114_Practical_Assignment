#
# Module Imports
from src.graph.graph_entities import GraphEntities
#
class CreateTransactionFunctions(object):
    """
    This class contains a number of transactions functions,
    focused on creation of nodes and relationships in the
    graph. The Merge statement is utilized to avoid duplication
    of Nodes/Relationships in the graph.

    According to Neo4j official docs, Transaction functions
    are the recommended form for containing transactional units
    of work. This form requires minimal boilerplate code and
    allows for a clear separation of database queries and
    application logic.

    Node Transaction Functions:
    """
    #
    @staticmethod
    def add_streamer(tx, name):
        """
        Add Streamer Node
        :param self:
        :param tx:
        :param name: Streamer Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        cql = "MERGE (s:"+supported_nodes[0]+" {name:$name}) " \
              "RETURN s;"
        tx.run(cql, name=name)
    #
    @staticmethod
    def add_viewer(tx, name):
        """
        Add Viewer Node
        :param self:
        :param tx:
        :param name: Viewer Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        cql = "MERGE (v:" + supported_nodes[1] + " {name:$name}) " \
              "RETURN v;"
        tx.run(cql, name=name)
    #
    @staticmethod
    def add_genre(tx, name):
        """
        Add Genre Node
        :param self:
        :param tx:
        :param name: Genre Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        cql = "MERGE (g:" + supported_nodes[2] + " {name:$name}) " \
              "RETURN g;"
        tx.run(cql, name=name)
    #
    @staticmethod
    def add_word(tx, name):
        """
        Add Word Node
        :param self:
        :param tx:
        :param name: Word Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        cql = "MERGE (w:" + supported_nodes[3] +" {name:$name}) " \
              "RETURN w;"
        tx.run(cql, name=name)
    #
    """
    Relationship Transaction Functions:
    """
    @staticmethod
    def add_uterrance(tx, name1, name2):
        """
        Add Utterance Relationship
        :param tx:
        :param name1: Streamer Node Name
        :param name2: Word Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        supported_relationships = GraphEntities.get_supported_relationship_types()
        cql = "MATCH (s:" + supported_nodes[0] + "),(w:" + supported_nodes[3] + ") " \
              "WHERE s.name=$name1 " \
              "AND w.name=$name2 " \
              "MERGE (s)-[u:" + supported_relationships[0] + "]-(w) " \
              "RETURN type(u);"
        tx.run(cql, name1=name1, name2=name2)
    #
    @staticmethod
    def add_comment(tx, name1, name2):
        """
        Add Comment Relationship
        :param tx:
        :param name1: Viewer Node Name
        :param name2: Word Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        supported_relationships = GraphEntities.get_supported_relationship_types()
        cql = "MATCH (v:" + supported_nodes[1] + "),(w:" + supported_nodes[3] + ") " \
              "WHERE v.name=$name1 " \
              "AND w.name=$name2 " \
              "MERGE (v)-[c:" + supported_relationships[1] + "]-(w) " \
              "RETURN type(c);"
        tx.run(cql, name1=name1, name2=name2)
    #
    @staticmethod
    def add_features(tx, name1, name2):
        """
        Add Feature Relationship
        :param tx:
        :param name1: Word Node Name
        :param name2: Genre Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        supported_relationships = GraphEntities.get_supported_relationship_types()
        cql = "MATCH (w:" + supported_nodes[3] +"),(g:" + supported_nodes[2] + ") " \
              "WHERE w.name=$name1 " \
              "AND g.name=$name2 " \
              "MERGE (w)-[f:" + supported_relationships[2] + "]-(g) " \
              "RETURN type(f);"
        tx.run(cql, name1=name1, name2=name2)
    #
    @staticmethod
    def add_follows(tx, name1, name2):
        """
        Add Follows Relationship
        :param tx:
        :param name1: Viewer Node Name
        :param name2: Genre Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        supported_relationships = GraphEntities.get_supported_relationship_types()
        cql = "MATCH (v:" + supported_nodes[1] + "),(g:" + supported_nodes[2] + ") " \
              "WHERE v.name=$name1 " \
              "AND g.name=$name2 " \
              "MERGE (w)-[f:" + supported_relationships[3] + "]-(g) " \
              "RETURN type(f);"
        tx.run(cql, name1=name1, name2=name2)
    #
    @staticmethod
    def add_partakes(tx, name1, name2):
        """
        Add Partakes Relationship
        :param tx:
        :param name1: Streamer Node Name
        :param name2: Genre Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        supported_relationships = GraphEntities.get_supported_relationship_types()
        cql = "MATCH (s:" + supported_nodes[0] + "),(g:" + supported_nodes[2] + ") " \
              "WHERE s.name=$name1 " \
              "AND g.name=$name2 " \
              "MERGE (s)-[p:" + supported_relationships[4] + "]-(g) " \
              "RETURN type(p);"
        tx.run(cql, name1=name1, name2=name2)
    #
    @staticmethod
    def add_subscribes(tx, name1, name2):
        """
        Add Subscribe Relationship
        :param tx:
        :param name1: Viewer Node Name
        :param name2: Streamer Node Name
        :return:
        """
        supported_nodes = GraphEntities.get_supported_node_types()
        supported_relationships = GraphEntities.get_supported_relationship_types()
        cql = "MATCH (v:" + supported_nodes[1] + "),(st:" + supported_nodes[0] + ") " \
              "WHERE v.name=$name1 " \
              "AND st.name=$name2 " \
              "MERGE (v)-[s:" + supported_relationships[5] + "]-(st) " \
              "RETURN type(s);"
        tx.run(cql, name1=name1, name2=name2)
#
class DeleteTransactionFunctions:
    """
    This class contains a number of transactions functions,
    focused on deletion of nodes and relationships in the
    graph.

    According to Neo4j official docs, Transaction functions
    are the recommended form for containing transactional units
    of work. This form requires minimal boilerplate code and
    allows for a clear separation of database queries and
    application logic.

    Relationship Transaction Functions:
    """
    #
    @staticmethod
    def delete_node(tx, node_value, node_type):
        """
        Delete node and all respective relationships
        :param tx:
        :param node_value:
        :param node_type:
        :return:
        """
        cql = "MATCH(n:" + node_type + "{name:$node_value}) DETACH DELETE(n);"
        tx.run(cql, node_value=node_value)
    #
    @staticmethod
    def delete_relationship(tx, node_value_1=None, node_value_2=None, node_type_1=None, node_type_2=None, relationship=None):
        """
        Delete Utterance Relationship, based on input nodes
        :param tx:
        :param name1: Streamer Node Name
        :param name2: Word Node Name
        :return:
        """
        if node_value_1 is None and node_type_1 is None:
            cql = "MATCH ()-[u:" + relationship + "]-(w:" + node_type_2 + "{name:$node_value_2}) " \
                  "DELETE u;"
            tx.run(cql, node_value_2=node_value_2)
        elif node_value_2 is None and node_type_2 is None:
            cql = "MATCH (s:" + node_type_1 + "{name:$node_value_1})-[u:" + relationship + "]-() " \
                  "DELETE u;"
            tx.run(cql, node_value_1=node_value_1)
        else:
            cql = "MATCH (s:" + node_type_1 + "{name:$node_value_1})-[u:" + relationship + "]-(w:" + node_type_2 + "{name:$node_value_2}) " \
                  "DELETE u;"
            tx.run(cql, node_value_1=node_value_1, node_value_2=node_value_2)