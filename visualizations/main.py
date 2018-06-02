from visualizations.visuals.piechart import PieChart
from visualizations.visuals.barchart import BarChart
from visualizations.visuals.wordcloud import WordCloudChart
from visualizations.visuals.linegraph import LineGraph
#
uri = "bolt://localhost:7687"
user = "neo4j"
password = "lol123"
save_path = "artifacts/"
pc = PieChart(uri=uri,
              user=user,
              password=password)
bc = BarChart(uri=uri,
              user=user,
              password=password)
wc = WordCloudChart(uri=uri,
                    user=user,
                    password=password)
lg = LineGraph()
#
"""
---------------------PIE CHARTS---------------------
"""
pc.draw_ratio_piechart(save_path=save_path + "Node_Distribution.html")
"""
---------------------BAR GRAPHS---------------------
"""
bc.draw_word_per_streamer(save_path=save_path + "Word_Streamer_Distribution.html")
#
bc.draw_word_per_platform(save_path=save_path + "Word_Platform_Distribution.html")
#
bc.draw_word_per_viewer(save_path=save_path + "Word_Viewer_Distribution.html")
#
bc.draw_word_per_genre(save_path=save_path + "Word_Genre_Distribution.html")
"""
---------------------WORD CLOUD---------------------
"""
try:
    wc.draw_ratio_wordcloud(save_path=save_path + "Word_Cloud.png")
except Exception as e:
    print("Word Cloud Graph was not plotted [" + str(e) + "]")
"""
---------------------LINE GRAPH---------------------
"""
load_path = "/home/gabriel/ICS5114_Practical_Assignment/visualizations/data/stats.txt"
lg.draw_resource_graph_CPU(load_path=load_path, save_path=save_path + "CPUResourceConsumption.html")
#
lg.draw_resource_graph_MEM_USAGE(load_path=load_path, save_path=save_path + "MainMemoryResourceConsumption.html")