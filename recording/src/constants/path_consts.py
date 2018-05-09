#
# Module imports
from pathlib import Path
import os.path as path
import os
#BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
BASE_DIR = path.abspath(path.join(__file__,"../.."))
PARENT_DIR = str(Path(BASE_DIR).parent)
#
# Directory Path Constants
DIR_VIDEO_BUFFER = BASE_DIR + "/video_buffer"
#
# File Path Constants
FILE_INPUT_CHANNELS = BASE_DIR + "/input_channels.json"
FILE_YOUTUBE_API_SECRET = BASE_DIR + "/client_secrets.json"
FILE_YOUTUBE_API_V3_DISCOVERYDOCUMENT = BASE_DIR + "/youtube-v3-discoverydocument.json"