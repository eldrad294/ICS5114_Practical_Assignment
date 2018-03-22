#
# Module imports
from pathlib import Path
import os
BASE_DIR = os.path.join(os.path.dirname(os.getcwd()))
PARENT_DIR = str(Path(BASE_DIR).parent)
#
# Directory Path Constants
#DIR_VIDEO_BUFFER = BASE_DIR + "/video_buffer"
DIR_VIDEO_BUFFER = "/video_buffer"
#
# File Path Constants
#FILE_INPUT_CHANNELS = BASE_DIR + "/config/input_channels.json"
FILE_INPUT_CHANNELS = "input_channels.json"



# print(FILE_INPUT_CHANNELS)  # Uncomment this string to test paths