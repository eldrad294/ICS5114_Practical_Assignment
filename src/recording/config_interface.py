#
# Module imports
from src.recording.config_object import ConfigObject
import json
#
class ConfigInterface:
    """"
    This class contains the required logic so as to
    integrate with online services. The class serves
    as a wrapper for the Streamlink video capture
    tool.
    """
    #
    def __init__(self, input_channels_path):
        """
        Default constructor
        :param input_channels_path: Path to input_channels.json
        """
        self.input_channels_path = input_channels_path
        self.input_channels = []
        self.load_input_channels()
    #
    def get_input_channels(self):
        """
        Returns input_channels
        :return:
        """
        return self.input_channels
    #
    def get_input_channel_size(self):
        """
        Return size of input_channels data structure
        :return:
        """
        return len(self.input_channels)
    #
    def load_input_channels(self):
        """
        Parse the input_channels.json file and stores
        each config structure as instances of the
        config_object_type. Each instance type is
        stored within a list.
        :return:
        """
        #
        # Read input_channel file and load content as a single json string
        file_input_channels = open(self.input_channels_path, 'r')
        json_string = json.load(file_input_channels)
        #
        # Iterate over json object
        for streams in json_string['streams']:
            temp_value = {}
            for attribute, value in streams.items():
                if attribute == "url":
                    temp_value[attribute.lower()] = value
                else:
                    temp_value[attribute.lower()] = value.lower()
            #
            co = ConfigObject(platform=temp_value['platform'],
                              url=temp_value['url'],
                              channel=temp_value['channel'],
                              genre=temp_value['genre'])
            self.input_channels.append(co)
        #
        print("Input channels loaded successfully -> Channel count: [" + str(self.get_input_channel_size()) + "]")
    #
    def display_input_channels(self):
        """
        Displays the input channels structure
        :return:
        """
        #
        if self.get_input_channel_size() != 0:
            [stream.display_details() for stream in self.input_channels]
        else:
            print("Input channels have not been loaded or might be corrupted!")

