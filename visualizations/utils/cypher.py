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
                return 'genres' as label,count, 'yellow' as color
                union all
                match(v:viewer)
                with count(v) as count
                return 'viewers' as label,count, 'black' as color;
               """
    #
    @staticmethod
    def cypher_word_per_streamer():
        return """
                match((s:streamer)-[u:utters]-(w:word))
                return  s.name as streamer, 
                count(u) as variety_count,
                sum(u.count) as tot_count;
               """
    #
    @staticmethod
    def cypher_word_per_platform():
        return """
                match((w:word)-[ut:utters]-(s:streamer)-[u:uses]-(p:platform))
                return  p.name as platform, 
                sum(ut.count) as tot_count, 
                count(ut.count) as variety_count;
               """
    #
    @staticmethod
    def cypher_word_per_viewer():
        return """
                match((v:viewer)-[c:comments]-(w:word))
                return  v.name as viewer, 
                count(c) as variety_count,
                sum(c.count) as tot_count;
               """
    #
    @staticmethod
    def cypher_word_per_genre():
        return """
                match((g:genre)-[p:partakes]-(s:streamer)-[u:utters]-(w:word))
                return g.name as genre, 
                sum(u.count) as tot_count, 
                count(u.count) as variety_count;
               """
    #
    @staticmethod
    def cypher_word_cloud():
        return """
                match(()-[c:comments]-(w:word)-[u:utters]-()) 
                return distinct w.name as word, 
                       (u.count + c.count) as count 
                order by count desc; 
               """