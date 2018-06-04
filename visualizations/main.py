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
load_path = "/home/gabriel/ICS5114_Practical_Assignment/visualizations/data/JohnOliverDockerStats.txt"
lg.draw_resource_graph_CPU_percentage(load_path=load_path, save_path=save_path + "CPU_Resource_Percentage_Consumption.html")
#
lg.draw_resource_graph_MEM_USAGE_percentage(load_path=load_path, save_path=save_path + "Main_Memory_Resource_Percentage_Consumption.html")
#
lg.draw_resource_graph_MEM_USAGE(load_path=load_path, save_path=save_path + "Main_Memory_Consumption.html")
#
lg.draw_resource_graph_NETIO_USAGE(load_path=load_path, save_path=save_path + "NET_IO_Consumption.html")
#
lg.draw_resource_graph_BLOCKIO_USAGE(load_path=load_path, save_path=save_path + "BLOCK_IO_Consumption.html")
#
load_path = "/home/gabriel/ICS5114_Practical_Assignment/visualizations/data/latency.csv"
lg.draw_resource_graph_latency(load_path=load_path, save_path=save_path + "GoogleConsole_Latency.html")
#
load_path = "/home/gabriel/ICS5114_Practical_Assignment/visualizations/data/traffic.csv"
lg.draw_resource_graph_traffic(load_path=load_path, save_path=save_path + "GoogleConsole_Traffic.html")