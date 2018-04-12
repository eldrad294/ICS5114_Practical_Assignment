class GraphEntities(object):
    #
    @staticmethod
    def get_supported_node_types():
        """
        Supported Node Types:

        :return:
        """
        return ("streamer", "viewer", "genre", "word")
    #
    @staticmethod
    def get_supported_relationship_types():
        """
        Supported Relationship Types:

        streamer - [UTTERS]     - word
        viewer   - [COMMENTS]   - word
        word     - [FEATURES]   - genre
        viewer   - [FOLLOWS]    - genre
        streamer - [PARTAKES]   - genre
        viewer   - [SUBCRIBES]  - streamer
        :return:
        """
        return ("utters","comments","features","follows","partakes","subscribes")