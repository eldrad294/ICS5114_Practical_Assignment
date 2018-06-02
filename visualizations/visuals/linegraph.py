from plotly.offline import plot
from plotly.graph_objs import *
import plotly.graph_objs as go
import pandas as pd
import numpy as np
#
class LineGraph():
    """
    Plots resource consumption in the form of a line graph
    , for multiple utilized resources
    """
    #
    def __init__(self):
        pass
    #
    def draw_resource_graph_CPU(self, load_path, save_path):
        """
        Plots Line Graph for CPU Usage
        :return:
        """
        df = self.__load_data(load_path)
        N = len(df)
        #print(df)
        x = np.linspace(0,1,N)
        df_kafka = df[df['NAME']=='kafka']
        df_storm = df[df['NAME']=='storm']
        df_neo4j = df[df['NAME']=='neo4j']
        df_producer1 = df[df['NAME'] == 'producer1']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['CPU'],
                mode='lines',
                name='Kafka CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['CPU'],
                mode='lines',
                name='Storm CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['CPU'],
                mode='lines',
                name='Neo4j CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer1['CPU'],
                mode='lines',
                name='Producer1 CPU Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource CPU Consumption",
            xaxis=dict(title="CPU Consumption Over Time"),
            yaxis=dict(title="CPU%")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_MEM_USAGE(self, load_path, save_path):
        """
        Plots Line Graph for CPU Usage
        :return:
        """
        df = self.__load_data(load_path)
        N = len(df)
        x = np.linspace(0, 1, N)
        df_kafka = df[df['NAME'] == 'kafka']
        df_storm = df[df['NAME'] == 'storm']
        df_neo4j = df[df['NAME'] == 'neo4j']
        df_producer1 = df[df['NAME'] == 'producer1']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['MEM'],
                mode='lines',
                name='Kafka MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['MEM'],
                mode='lines',
                name='Storm MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['MEM'],
                mode='lines',
                name='Neo4j MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer1['MEM'],
                mode='lines',
                name='Producer1 MEM Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource Main Memory Usage",
            xaxis=dict(title="Main Memory Usage Over Time"),
            yaxis=dict(title="Main Memory % Consumption")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def __load_data(self, load_path):
        """
        Loads data from file
        :return:
        """
        data = pd.read_fwf(load_path, sep=" ")
        return data.fillna('')

