#
# Module Imports
from streamparse import Grouping, Topology
from spouts.video_recorder import VideoRecorder
from bolts.video_decoder import VideoDecoder
#
class MainTopology(Topology):
    """
    Storm Topology
    """
    #
    # variable declaration
    parallel_degree = 1
    #
    print('Starting Topology..')
    video_recording_spout = VideoRecorder.spec()
    #
    count_bolt = VideoDecoder.spec(inputs={video_recording_spout: Grouping.fields('video')}
                                   , par=parallel_degree)