#
# Module imports
import hashlib
#
class ConfigObject:
    """
    The class template for the input channel json structure
    """
    #
    def __init__(self, platform, src, channel, genre, type):
        self.platform = platform
        self.src = src
        self.channel = channel
        self.genre = genre
        self.type = type
        self.id = self.get_hash()
    #
    def get_hash(self):
        """
        Calculates a unique hash based off input platform, channel and type combined
        https://www.pythoncentral.io/hashing-strings-with-python/
        """
        return hashlib.md5((self.platform + self.channel + self.type).encode()).hexdigest()
    #
    def get_details(self):
        """"
        Returns instance details in the form of a dictionary
        """
        detail_dict = {"platform": self.platform,
                       "src": self.src,
                       "channel": self.channel,
                       "genre": self.genre,
                       "type": self.type,
                       "id": self.id}
        return detail_dict
    #
    def display_details(self):
        """
        Pretty print instance details
        """
        print("Platform: " + str(self.platform) +
              "\nSrc: " + str(self.src) +
              "\nChanel: " + str(self.channel) +
              "\nGenre: " + str(self.genre) +
              "\nType: " + str(self.type) +
              "\nId: " + str(self.id))
    #
    def get_src_type(self):
        """
        Returns the type of src which will be utilized

        Return 0 if src is a livestream source and video
        Return 1 if src is not a livestream source and video
        Return 2 if src is a livestream source and text
        Return 3 if src is not a livestream source and text
        :return: Integer
        """
        non_livestream_platforms = ('youtube')
        src_types=('video','text')
        #
        if self.platform in non_livestream_platforms:
            if self.type == src_types[0]:
                return 1
            elif self.type == src_types[1]:
                return 3
            else:
                return -1
        else:
            if self.type == src_types[0]:
                return 0
            elif self.type == src_types[1]:
                return 2
            else:
                return -1