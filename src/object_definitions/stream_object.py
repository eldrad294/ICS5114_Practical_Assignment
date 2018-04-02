#
# Module Imports
class StreamObject:
    """
    Object which will form the basis off all stream messages
    produced and offloaded downstream through the pipeline.

    This object type is intended to be serialized and pushed onto
    the Kafka broker, which will eventually be picked by the
    Storm Spout/ Kapfka Consumer, de-serialized and pushed down
    the pipeline into Storm.
    """
    #
    def __init__(self, platform, src_url, channel, genre, time_stamp,
                 file_path, cloud_url, file=None):
        self.platform = platform
        self.src_url = src_url
        self.channel = channel
        self.genre = genre
        self.file_path = file_path
        self.file = file
        self.cloud_url = cloud_url
        self.time_stamp = time_stamp
    #
    def get_details(self):
        """"
        Returns instance details in the form of a dictionary
        """
        detail_dict = {"platform": self.platform,
                       "Source URL": self.src_url,
                       "Cloud URL":self.cloud_url,
                       "file path": self.file_path,
                       "file": self.file,
                       "channel": self.channel,
                       "genre": self.genre,
                       "time_stamp": self.time_stamp}
        return detail_dict

    #
    def display_details(self):
        """
        Pretty print instance details
        """
        print("Platform: " + str(self.platform) +
              "\nSource URL: " + str(self.src_url) +
              "\nCloud URL:" + str(self.cloud_url) +
              "\nFile Path: " + str(self.file_path) +
              "\nChanel: " + str(self.channel) +
              "\nGenre: " + str(self.genre) +
              "\nTime Stamp: " + str(self.time_stamp))