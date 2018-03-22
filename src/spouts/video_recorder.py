#
# Module Imports
from streamparse import Spout
from interfaces.config_interface import ConfigInterface
from interfaces.recording_interface import RecordingInterface
from constants import path_consts as pc
#
class VideoRecorder(Spout):
    """
    Storm Spout Logic

    Responsible for offloading data off streaming websites,
    and emits data as a a series of chuncked videos down
    the topology pipeline.
    """
    #
    outputs = ['video'] #Grouping Mechanism
    #
    def initialize(self, storm_conf, context):
        """
        Storm Spout 'constructor method'
        :param storm_conf:
        :param context:
        :return:
        """
        print("SPOUT HAS BEEN INITIALIZED!!")
        # Loads config from input_channels.json
        self.ci = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
        #
        # Records video streams to disk locally
        self.ri = RecordingInterface(config_obj=self.ci.get_input_channels()[2],
                                     segment_time_span=30,
                                     extension="wav",
                                     quality="worst")
    #
    def next_tuple(self):
        """
        Submitter method for Spout, emits captured
        and segmented video file paths
        :return:
        """
        print("SPOUT IS EMITTING!!")
        segment_video_path = self.ri.capture_and_return()
        if segment_video_path is not None:
            print(segment_video_path)
            self.emit([segment_video_path])