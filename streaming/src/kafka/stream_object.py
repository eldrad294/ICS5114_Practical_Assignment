class StreamObject:
    """
    Object which will form the basis off all stream messages produced and offloaded downstream through the pipeline.

    This object type is intended to be serialized and pushed onto the Kafka broker, which will eventually be picked by
    the Storm Spout/ Kapfka Consumer, de-serialized and pushed down the pipeline into Storm.
    """
    def __init__(self, platform, src_url, channel, genre, time_stamp, file_path, cloud_bucket_name, cloud_bucket_path,
                 text=None):
        """
        Constructor
        :param platform:            Retrieved from config_object
        :param src_url:             Retrieved from config_object
        :param channel:             Retrieved from config_object
        :param genre:               Retrieved from config_object
        :param time_stamp:          Retrieved from config_object
        :param file_path:           Set to 'None' if extracting text
        :param cloud_bucket_name:   Set to 'None' if extracting text
        :param cloud_bucket_path:   Set to 'None' if extracting text
        :param text:
        """
        self.platform = platform
        self.src_url = src_url
        self.channel = channel
        self.genre = genre
        self.file_path = file_path
        self.cloud_bucket_name = cloud_bucket_name
        self.cloud_bucket_path = cloud_bucket_path
        self.time_stamp = time_stamp
        self.text = text
        self.detail_dict = {"platform": self.platform,
                            "source_url": self.src_url,
                            "cloud_bucket_name":self.cloud_bucket_name,
                            "cloud_bucket_path":self.cloud_bucket_path,
                            "file_path": self.file_path,
                            "channel": self.channel,
                            "genre": self.genre,
                            "time_stamp": self.time_stamp,
                            "text": self.text}

    def get_details(self, key=None):
        """
        :param key: Optional ID, if unspecified, all the dictionary collection will be returned
        :return:    Returns instance details in the form of a dictionary
        """
        if key is None:
            return self.detail_dict
        else:
            return self.detail_dict[key]

    def display_details(self):
        """
        Pretty print instance details
        """
        print("Platform: " + str(self.platform) +
              "\nSource URL: " + str(self.src_url) +
              "\nCloud Bucket Name:" + str(self.cloud_bucket_name) +
              "\nCloud Bucket Path:" + str(self.cloud_bucket_path) +
              "\nFile Path: " + str(self.file_path) +
              "\nChanel: " + str(self.channel) +
              "\nGenre: " + str(self.genre) +
              "\nTime Stamp: " + str(self.time_stamp))
