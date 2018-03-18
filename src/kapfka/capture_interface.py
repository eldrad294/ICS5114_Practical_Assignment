#
# Module imports
from src.object_definitions import config_object
#
class CaptureInterface:
    """"
    This class contains the required logic so as to
    integrate with online services. The class serves
    as a wrapper for the Streamlink video capture
    tool.
    """
    def __init__(self, input_channels_path, capture_path):
        self.input_channels_path = input_channels_path
        self.capture_path = capture_path
    #
