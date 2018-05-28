from visualizations.visuals.piechart import PieChart
from visualizations.visuals.barchart import BarChart
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