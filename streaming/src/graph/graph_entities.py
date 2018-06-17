class GraphEntities(object):
    @staticmethod
    def get_supported_node_types():
        """
        :return: Return all the supported GraphDB node types
        """
        return ("streamer", "viewer", "genre", "word", "platform")

    @staticmethod
    def get_supported_relationship_types():
        """
        Supported Relationship Types:
        streamer - [UTTERS]     - word
        viewer   - [COMMENTS]   - word
        word     - [FEATURES]   - genre
        viewer   - [FOLLOWS]    - genre
        streamer - [PARTAKES]   - genre
        viewer   - [SUBSCRIBES] - streamer
        streamer - [USES]       - platform
        :return: Returns all the supported GraphDB relationship types
        """
        return ("utters", "comments", "features", "follows", "partakes", "subscribes", "uses")
