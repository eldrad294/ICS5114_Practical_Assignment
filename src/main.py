#
# Main Class, which controls entire routine
#
# Module Imports
from src.kapfka.config_interface import ConfigInterface
from src.kapfka.recording_interface import RecordingInterface
from src.constants import path_consts as pc
#
# Loads config from input_channels.json
ci = ConfigInterface(input_channels_path=pc.FILE_INPUT_CHANNELS)
#
# Records video streams to disk locally
ri = RecordingInterface(config_obj=ci.get_input_channels()[2],
                        segment_time_span=300,
                        extension="wav",
                        quality="worst")
ri.capture()
