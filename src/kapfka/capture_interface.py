#
# Module imports
from src.object_definitions import config_object
import json
#
class CaptureInterface:
    """"
    This class contains the required logic so as to
    integrate with online services. The class serves
    as a wrapper for the Streamlink video capture
    tool.
    """
    #
    def __init__(self, input_channels_path, video_buffer_path):
        self.input_channels_path = input_channels_path
        self.video_buffer_path = video_buffer_path
        self.input_channels = []
        self.load_input_channels()
    #
    def load_input_channels(self):
        """
        Parse the input_channels.json file and stores
        each config structure as instances of the
        config_object_type. Each instance type is
        stored within a list.
        """
        #
        # Read input_channel file and load content as a single json string
        file_input_channels = open(self.input_channels_path, 'r')
        json_string = json.load(file_input_channels)
        #
        # Iterate over json object
        for streams in json_string['streams']:
            temp_value = []
            for attribute, value in streams.items():
                temp_value.append(value)
            #
            co = config_object.ConfigObject(temp_value[0],
                                            temp_value[1],
                                            temp_value[2],
                                            temp_value[3])
            self.input_channels.append(co)
    #
    def display_input_channels(self):
        """
        Displays the input channels structure
        """
        #
        if len(self.input_channels) != 0:
            [stream.display_details() for stream in self.input_channels]
        else:
            print("Input channels have not been loaded or might be corrupted!")
