#
# Module imports
import hashlib
#
class ConfigObject:
    """
    The class template for the input channel json structure
    """
    #
    def __init__(self, platform, src, channel, genre):
        self.platform = platform
        self.src = src
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
                       "src": self.src,
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
              "\nsrc: " + str(self.src) +
              "\nChanel: " + str(self.channel) +
              "\nGenre: " + str(self.genre) +
              "\nId: " + str(self.id))
    #
    def get_src_type(self):
        """
        Returns the type of src which will be utilized

        Return 0 if src is an online source
        Return 1 if src is a local source
        :return: Integer
        """
        identifier_list = ["http://","https://"]
        #
        for identifier in identifier_list:
            if identifier in self.src:
                return 0
        #
        return 1