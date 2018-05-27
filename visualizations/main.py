from visualizations.visuals.piechart import PieChart
from visualizations.visuals.barchart import BarChart
#
uri = "bolt://localhost:7687"
user = "neo4j"
password = "lol123"
save_path = "artifacts/"
#
PieChart().draw_ratio_piechart(uri=uri,
                               user=user,
                               password=password,
                               save_path=save_path + "Node_Distribution.html")
#
BarChart().draw_word_per_streamer(uri=uri,
                                  user=user,
                                  password=password,
                                  save_path=save_path + "Word_Streamer_Distribution.html")