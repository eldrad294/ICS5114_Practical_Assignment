#
# Module Imports
from streamparse import Bolt
import os
#
class VideoDecoder(Bolt):
    """
    This bolt contains the logic to recieve segmented
    video file paths, opens the respective file,
    and decodes the video speech audio into text.

    The decoded text is emitted to another bolt.
    """
    #
    # Grouping Mechanism
    outputs = ['video']
    #
    def initialize(self, conf, ctx):
        """
        video decoder initialize method
        :param conf:
        :param ctx:
        :return:
        """
        pass
    #
    def process(self, tup):
        """
        Decodes segment video into text, and emits that text
        :param tup:
        :return:
        """
        streaming_object = tup.values[0]
        #
        if not streaming_object:
            return
        self.log("Received streaming object for URI: " + str(streaming_object['cloud_bucket_path']))
        #
        decoded_video_string = streaming_object # VIDEO DECODING LOGIC GOES HERE
        #
        self.log("Video decoding for [" + str(streaming_object['cloud_bucket_path']) +
                 "] complete - Pushing downstream.. ")
        self.emit([decoded_video_string])