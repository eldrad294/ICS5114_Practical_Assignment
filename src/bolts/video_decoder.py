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
    def initialize(self, conf, ctx):
        """
        Storm Bolt 'constructor method'
        :param conf:
        :param ctx:
        :return:
        """
        self.pid = os.getpid()
    #
    def process(self, tup):
        """
        Decodes segment video into text, and emits that text
        :param tup:
        :return:
        """
        print(tup)
        pass