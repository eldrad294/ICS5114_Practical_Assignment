#
# Module Imports
import nltk
from streamparse import Grouping, Topology
from spouts.video_recorder import VideoRecorder
from spouts.text_recorder import TextRecorder
from bolts.video_decoder import VideoDecoder
from bolts.text_decoder import TextDecoder
from bolts.graph_writer import GraphWriter

# Ensure required nltk resources are present
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class MainTopology(Topology):
    """
    Storm Topology
    """
    #
    # variable declaration
    print('Starting Topology..')
    video_spout_parallel_degree = 1
    text_spout_parallel_degree = 1
    video_decoder_parallel_degree = 4
    text_decoder_parallel_degreee = 1
    graph_writer_parallel_degree = 2
    #
    print('Initiating Spouts..')
    video_recording_spout = VideoRecorder.spec(par=video_spout_parallel_degree)
    text_recording_spout = TextRecorder.spec(par=text_spout_parallel_degree)
    #
    print('Initiating Decoder Bolts..')
    video_decoder_bolt = VideoDecoder.spec(inputs={video_recording_spout: Grouping.fields('video')}
                                           , par=video_decoder_parallel_degree)
    text_decoder_bolt = TextDecoder.spec(inputs={text_recording_spout: Grouping.fields('text')}
                                           , par=text_decoder_parallel_degreee)
    #
    print('Initiating GraphWriter Bolt..')
    graph_writer_bolt = GraphWriter.spec(inputs={video_decoder_bolt: Grouping.fields('video'),
                                                 text_decoder_bolt: Grouping.fields('text')}
                                         , par=graph_writer_parallel_degree)