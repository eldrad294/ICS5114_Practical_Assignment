#
# Module imports
import hashlib
#
class ConfigObject:
    """
    The class template for the input channel json structure
    """
    #
    def __init__(self, platform, url, channel, genre):
        self.platform = platform
        self.url = url
        self.channel = channel
        self.genre = genre
        self.id = self.get_hash()
    #
    def get_hash(self):
        """
        Calculates a unique hash based off input platform and channel combined
        https://www.pythoncentral.io/hashing-strings-with-python/
        """
        return hashlib.md5((self.platform + self.channel).encode()).hexdigest()
    #
    def get_details(self):
        """"
        Returns instance details in the form of a dictionary
        """
        detail_dict = {"platform": self.platform,
                       "url": self.url,
                       "channel": self.channel,
                       "genre": self.genre,
                       "id": self.id}
        return detail_dict
    #
    def display_details(self):
        """
        Pretty print instance details
        """
        print("Platform: " + str(self.platform) +
              "\nURL: " + str(self.url) +
              "\nChanel: " + str(self.channel) +
              "\nGenre: " + str(self.genre) +
              "\nId: " + str(self.id))