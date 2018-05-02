#
# Module Imports
from streamparse import Grouping, Topology
from spouts.video_recorder import VideoRecorder
from bolts.video_decoder import VideoDecoder
from bolts.graph_writer import GraphWriter
#
class MainTopology(Topology):
    """
    Storm Topology
    """
    #
    # variable declaration
    spout_parallel_degree = 1
    video_decoder_parallel_degree = 1
    graph_writer_parallel_degree = 1
    #
    print('Starting Topology..')
    video_recording_spout = VideoRecorder.spec()
    #
    video_decoder_bolt = VideoDecoder.spec(inputs={video_recording_spout: Grouping.fields('video')}
                                           , par=video_decoder_parallel_degree)
    #
    graph_writer_bolt = GraphWriter.spec(inputs={video_decoder_bolt: Grouping.fields('video')}
                                         , par=graph_writer_parallel_degree)