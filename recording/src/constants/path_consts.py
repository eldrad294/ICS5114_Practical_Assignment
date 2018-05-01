#
# Module imports
from pathlib import Path
import os
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
PARENT_DIR = str(Path(BASE_DIR).parent)
#
# Directory Path Constants
DIR_VIDEO_BUFFER = BASE_DIR + "/video_buffer"
#
# File Path Constants
FILE_INPUT_CHANNELS = BASE_DIR + "/input_channels.json"
#FILE_INPUT_CHANNELS = "input_channels.json"