import os.path as path
from pathlib import Path

BASE_DIR = path.abspath(path.join(__file__, "../.."))
PARENT_DIR = str(Path(BASE_DIR).parent)

# Directory Path Constants
DIR_VIDEO_BUFFER = BASE_DIR + "/video_buffer"

# File Path Constants
FILE_INPUT_CHANNELS = BASE_DIR + "/input_channels.json"
FILE_YOUTUBE_API_SECRET = BASE_DIR + "/client_secrets.json"
FILE_YOUTUBE_API_V3_DISCOVERYDOCUMENT = BASE_DIR + "/youtube-v3-discoverydocument.json"
