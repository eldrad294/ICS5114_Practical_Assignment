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
    #
    @staticmethod
    def cypher_foul_word_streamer():
        return """
               match((s:streamer)-[u:utters]-(w:word)) 
               where w.foul_flag=true 
               return s.name as streamer,sum(u.count) as tot_foul 
               order by tot_foul desc 
               limit 20; 
               """
    #
    @staticmethod
    def cypher_foul_word_viewer():
        return """
               match ((v:viewer)-[c:comments]-(w:word)) 
               where w.foul_flag=true 
               return v.name as viewer, sum(c.count) as tot_foul 
               order by tot_foul desc 
               limit 20;
               """
    #
    @staticmethod
    def cypher_foul_word_platform():
        """
        As of current time, cypher does not support post union processing.
        Therefore we return subsets of union and sum them through python.
        """
        return """
               match((p:platform)-[us:uses]-(s:streamer)-[u:utters]-(w:word)) 
               where w.foul_flag=true 
               return p.name as platform,count(us) as tot_foul 
               union 
               match((p:platform)-[us:uses]-(s:streamer)-[su:subscribes]-(v:viewer)-[c:comments]-(w:word))
               where w.foul_flag=true
               return p.name as platform, sum(c.count) as tot_foul
               order by tot_foul desc
               limit 20;
               """
    #
    @staticmethod
    def cypher_foul_word_genre():
        """
        As of current time, cypher does not support post union processing.
        Therefore we return subsets of union and sum them through python.
        """
        return """
               match((g:genre)-[p:partakes]-(s:streamer)-[u:utters]-(w:word)) 
               where w.foul_flag=true 
               return g.name as genre, count(g) as tot_foul 
               union 
               match((g:genre)-[p:partakes]-(s:streamer)-[su:subscribes]-(v:viewer)-[c:comments]-(w:word))
               where w.foul_flag=true
               return g.name as genre, sum(c.count) as tot_foul
               order by tot_foul desc
               limit 20;
               """
    #
    @staticmethod
    def cypher_viewer_word_relationship(viewer):
        if viewer is None:
            return """
                   match((v:viewer)-[c:comments]-(w:word))  
                    return v.name as viewer,
                    c.count as comment_count,
                    w.name as word,
                    w.foul_flag as foul_flag
                    order by comment_count desc
                    limit 100;
                   """
        else:
            return ("match((v:viewer)-[c:comments]-(w:word)) "
                    "where v.name = '" + str(viewer) + "' "
                    "return v.name as viewer, "
                    "c.count as comment_count, "
                    "w.name as word, "
                    "w.foul_flag as foul_flag "
                    "order by comment_count desc "
                    "limit 100;")
        #
    @staticmethod
    def cypher_top_n_foul_words():
        return """
               match((w:word)-[u:utters]-(s:streamer)),
                    ((w:word)-[c:comments]-(v:viewer)) 
               where w.foul_flag=true 
               return w.name as word_name, count(w) as foul_word_count 
               order by foul_word_count desc;
               """