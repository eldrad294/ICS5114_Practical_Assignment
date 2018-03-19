#
# Main Class, which controls entire routine
#
# Module Imports
from src.kapfka.capture_interface import CaptureInterface
from src.constants import path_consts as pc
#
ci = CaptureInterface(input_channels_path=pc.FILE_INPUT_CHANNELS,
                      video_buffer_path=pc.DIR_VIDEO_BUFFER)
ci.display_input_channels()
