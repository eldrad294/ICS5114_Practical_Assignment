import os
import configparser


class BDAConfigParser:
    """
    Class responsible for parsing the main configuration file.
    """
    #################
    # Private members
    __config = None
    #################

    def __init__(self, config_file_path):
        """
        Constructor.
        :param config_file_path: Absolute path to the configuration file. Config file is expected to follow the
                                 standard INI file format.
        """
        self.reload_config_file(config_file_path)

    def reload_config_file(self, config_file_path):
        """
        Reload configuration file.
        :param config_file_path: Absolute path to the configuration file. Config file is expected to follow the
                                 standard INI file format.
        :return:                 None.
        """
        #self.__validation(config_file_path) # Disabled valdiation, since this was conflicting with Storm Topology Setup
        self.__config = configparser.ConfigParser()
        self.__config.read(config_file_path)

    def get_value(self, section_name, key_name):
        """
        Retrieve configuration value.
        :param section_name: Config section name.
        :param key_name:     Config key name.
        :return:             Config value.
        """
        result = None
        if section_name in self.__config and key_name in self.__config[section_name]:
            result = self.__config[section_name][key_name]
        return result

    @staticmethod
    def __validation(config_file_path):
        """
        Validation.
        :param config_file_path: Absolute path to the configuration file.
        :return:                 None.
        :raises                  ValueError in case config file does not exist.
        """
        if not os.path.isfile(config_file_path):
            raise ValueError('File not found.')


# ToDo: Consider converting this class into a Singleton.
#config_file = os.getcwd() + '/src/config.ini'
config_file = os.path.dirname(__file__) + "/../config.ini"
g_config = BDAConfigParser(config_file)
