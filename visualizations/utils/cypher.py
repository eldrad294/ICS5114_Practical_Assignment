class Cypher():
    """
    A class with cypher queries dedicated to visualizations
    """
    @staticmethod
    def cypher_ratio_piechart():
        return """
                match(s:streamer) 
                with count(s) as count 
                return 'streamers' as label, count, 'red' as color
                union all
                match(p:platform)
                with count(p) as count
                return 'platforms' as label, count, 'blue' as color
                union all
                match(w:word)
                with count(w) as count
                return 'words' as label ,count, 'green' as color
                union all
                match(g:genre)
                with count(g) as count
                return 'genres' as label,count, 'yellow' as color;
               """
    #
    @staticmethod
    def cypher_words_per_streamer():
        return """
                match((s:streamer)-[u:utters]-(w:word))
                return s.name as streamer, count(u) as count;
               """