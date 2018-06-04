from plotly.offline import plot
from plotly.graph_objs import *
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
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
    def draw_resource_graph_CPU_percentage(self, load_path, save_path):
        """
        Plots Line Graph for CPU% Usage
        :return:
        """
        df = self.__load_data_txt(load_path)
        x = np.linspace(0, 510) #510 minutes
        df_kafka = df[df['NAME']=='kafka']
        df_storm = df[df['NAME']=='storm']
        df_neo4j = df[df['NAME']=='neo4j']
        df_producer2 = df[df['NAME'] == 'producer2']
        df_producer3 = df[df['NAME'] == 'producer3']
        df_producer4 = df[df['NAME'] == 'producer4']
        df_producer5 = df[df['NAME'] == 'producer5']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['CPU %'],
                mode='lines',
                name='Kafka CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['CPU %'],
                mode='lines',
                name='Storm CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['CPU %'],
                mode='lines',
                name='Neo4j CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer2['CPU %'],
                mode='lines',
                name='Producer2 CPU Usage'
            )
            ,
            go.Scatter(
                x=x,
                y=df_producer3['CPU %'],
                mode='lines',
                name='Producer3 CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer4['CPU %'],
                mode='lines',
                name='Producer4 CPU Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer5['CPU %'],
                mode='lines',
                name='Producer5 CPU Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource CPU % Consumption",
            xaxis=dict(title="CPU Consumption Over Time (Minutes Elapsed)"),
            yaxis=dict(title="CPU%")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_MEM_USAGE_percentage(self, load_path, save_path):
        """
        Plots Line Graph for Mem% Usage
        :return:
        """
        df = self.__load_data_txt(load_path)
        x = np.linspace(0, 510) #510 minutes
        df_kafka = df[df['NAME'] == 'kafka']
        df_storm = df[df['NAME'] == 'storm']
        df_neo4j = df[df['NAME'] == 'neo4j']
        df_producer2 = df[df['NAME'] == 'producer2']
        df_producer3 = df[df['NAME'] == 'producer3']
        df_producer4 = df[df['NAME'] == 'producer4']
        df_producer5 = df[df['NAME'] == 'producer5']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['MEM %'],
                mode='lines',
                name='Kafka MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['MEM %'],
                mode='lines',
                name='Storm MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['MEM %'],
                mode='lines',
                name='Neo4j MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer2['MEM %'],
                mode='lines',
                name='Producer2 MEM Usage'
            )
            ,
            go.Scatter(
                x=x,
                y=df_producer3['MEM %'],
                mode='lines',
                name='Producer3 MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer4['MEM %'],
                mode='lines',
                name='Producer4 MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer5['MEM %'],
                mode='lines',
                name='Producer5 MEM Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource Main Memory % Usage",
            xaxis=dict(title="Main Memory Usage Over Time (Minutes Elapsed)"),
            yaxis=dict(title="Main Memory % Consumption")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_MEM_USAGE(self, load_path, save_path):
        """
        Plots Line Graph for Memory Usage
        :return:
        """
        df = self.__load_data_txt(load_path)
        x = np.linspace(0, 510) #510 minutes
        df_kafka = df[df['NAME'] == 'kafka']
        df_storm = df[df['NAME'] == 'storm']
        df_neo4j = df[df['NAME'] == 'neo4j']
        df_producer2 = df[df['NAME'] == 'producer2']
        df_producer3 = df[df['NAME'] == 'producer3']
        df_producer4 = df[df['NAME'] == 'producer4']
        df_producer5 = df[df['NAME'] == 'producer5']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Kafka MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Storm MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Neo4j MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer2['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer2 MEM Usage'
            )
            ,
            go.Scatter(
                x=x,
                y=df_producer3['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer3 MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer4['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer4 MEM Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer5['MEM USAGE / LIMIT'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer5 MEM Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource Main Memory Usage",
            xaxis=dict(title="Main Memory Usage Over Time (Minutes Elapsed)"),
            yaxis=dict(title="Main Memory Consumption")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_NETIO_USAGE(self, load_path, save_path):
        """
        Plots Line Graph for NET I/O Usage
        :return:
        """
        df = self.__load_data_txt(load_path)
        x = np.linspace(0, 510)  # 510 minutes
        df_kafka = df[df['NAME'] == 'kafka']
        df_storm = df[df['NAME'] == 'storm']
        df_neo4j = df[df['NAME'] == 'neo4j']
        df_producer2 = df[df['NAME'] == 'producer2']
        df_producer3 = df[df['NAME'] == 'producer3']
        df_producer4 = df[df['NAME'] == 'producer4']
        df_producer5 = df[df['NAME'] == 'producer5']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Kafka NET I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Storm NET I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Neo4j NET I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer2['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer2 NET I/O Usage'
            )
            ,
            go.Scatter(
                x=x,
                y=df_producer3['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer3 NET I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer4['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer4 NET I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer5['NET I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer5 NET I/O Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource NET I/O Usage",
            xaxis=dict(title="NET I/O Usage Over Time (Minutes Elapsed)"),
            yaxis=dict(title="NET I/O Usage")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_BLOCKIO_USAGE(self, load_path, save_path):
        """
        Plots Line Graph for BLOCK I/O Usage
        :return:
        """
        df = self.__load_data_txt(load_path)
        x = np.linspace(0, 510)  # 510 minutes
        df_kafka = df[df['NAME'] == 'kafka']
        df_storm = df[df['NAME'] == 'storm']
        df_neo4j = df[df['NAME'] == 'neo4j']
        df_producer2 = df[df['NAME'] == 'producer2']
        df_producer3 = df[df['NAME'] == 'producer3']
        df_producer4 = df[df['NAME'] == 'producer4']
        df_producer5 = df[df['NAME'] == 'producer5']
        #
        data = Data([
            go.Scatter(
                x=x,
                y=df_kafka['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Kafka BLOCK I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_storm['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Storm BLOCK I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_neo4j['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Neo4j BLOCK I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer2['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer2 BLOCK I/O Usage'
            )
            ,
            go.Scatter(
                x=x,
                y=df_producer3['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer3 BLOCK I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer4['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer4 BLOCK I/O Usage'
            ),
            go.Scatter(
                x=x,
                y=df_producer5['BLOCK I/O'].apply(self.__convert_to_kb),
                mode='lines',
                name='Producer5 BLOCK I/O Usage'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Resource BLOCK I/O Usage",
            xaxis=dict(title="BLOCK I/O Usage Over Time (Minutes Elapsed)"),
            yaxis=dict(title="BLOCK I/O Usage")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_latency(self, load_path, save_path):
        """
        Plots line graph for google console latency measures

        :param load_path:
        :return:
        """
        df = self.__load_data_csv(load_path,['time','Median','98th percentile (slowest 2%)'])
        df_time = df[['time']]
        df_median = df[['Median']]
        df_percentile_quarter = df[['98th percentile (slowest 2%)']]
        data = Data([
            go.Scatter(
                x=df_time['time'],
                y=df_median['Median'],
                mode='lines',
                name='Google Console Median Latency'
            ),
            go.Scatter(
                x=df_time['time'],
                y=df_percentile_quarter['98th percentile (slowest 2%)'].apply(self.__convert_to_kb),
                mode='lines',
                name='Google Console 98th percentile (slowest 2%) Latency'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Google Console Latency Usage",
            xaxis=dict(title="Time Elapsed"),
            yaxis=dict(title="Latency Score (ms)")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def draw_resource_graph_traffic(self, load_path, save_path):
        """
        Plots line graph for google console traffic measures

        :param load_path:
        :return:
        """
        df = self.__load_data_csv(load_path, ['time','traffic'])
        df_time = df[['time']]
        df_traffic = df[['traffic']]
        data = Data([
            go.Scatter(
                x=df_time['time'],
                y=df_traffic['traffic'],
                mode='lines',
                name='Google Console traffic'
            )
        ])
        layout = go.Layout(
            barmode='group',
            title="Google Console Traffic Activity",
            xaxis=dict(title="Time Elapsed"),
            yaxis=dict(title="Traffic (request/sec)")
        )
        config = None
        fig = go.Figure(data=data, layout=layout)
        plot(fig, config=config, filename=save_path)
    #
    def __load_data_txt(self, load_path):
        """
        Loads data from text file
        :return:
        """
        data = pd.read_fwf(load_path, sep=" ")
        return data.fillna('')
    #
    def __load_data_csv(self, load_path, column_names):
        """
        Loads data from csv file
        :return:
        """
        data = pd.read_csv(load_path, names=column_names)
        return data
    #
    def __convert_to_kb(self, input_value):
        """
        Function which receives input size, and convert into KB

        Receives input of following format:
        eg: 365.5MiB / 2GiB

        and returns it as follows
        [374272 KB , 2097152 KB]
        :param value:
        :return:
        """
        stripped_value = input_value.replace(' ','')
        values = stripped_value.split('/')
        metrics = {'kB':'1','MB':'1024','MiB':'1024','GiB':'1048576','GB':'1048576'}
        return_list = []
        for value in values:
            value = str(value)
            for key, val in metrics.items():
                if key in value:
                    value = value.replace(key, '')
                    value = float(value) * float(metrics[key])
                    break
            return_list.append(value)
        return return_list[0]



