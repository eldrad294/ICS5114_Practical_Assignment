import os
import time
import shutil
from uuid import getnode
from abc import ABC, abstractmethod

from src.coding_framework.BDAConfigParser import g_config
from src.speech_recognition.BDAVideoAudioUtilities import BDAVideoToAudio

from google.cloud import speech
from google.cloud import storage
from google.cloud.speech import types


# Class hierarchy
# ---------------
#                                                      +---------------------+
#                                                      |  GoogleStorageBase  |
#                                                      +----------+----------+
#                                                                 ^
#                                                                 |
#                                                                 |
#                                                                 |
#                                   +-----------------------------+-----------------------------+
#                                   |                                                           |
#                   +---------------+--------------------+                  +-------------------+------------------+
#                   | BDAGoogleStorageUploadAbstractBase |                  |  BDAGoogleStorageUploadAbstractBase  |
#                   +---------------+--------------------+                  +--------------------------------------+
#                                   ^
#                                   |
#                                   |
#               +-------------------+-------------------+
#               |                                       |
# +-------------+-------------------+   +---------------+-----------+
# |  BDAGoogleStorageConvertUpload  |   |  BDAGoogleStorageConsume  |
# +---------------------------------+   +---------------------------+
#


class GoogleStorageBase(ABC):
    def __init__(self):
        """
        Constructor
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__()
        self.__load_env_variables()
        self.__ensure_bucket_availability()

    def __load_env_variables(self):
        """
        Google Speech Recognition requires a 'GOOGLE_APPLICATION_CREDENTIALS' environment variable, pointing to the
        JSON file containing the relevant credentials.
        In case the mentioned environment variable is not present, this method creates it by extracting the relevant
        information from the main config file through BDAConfigParser.
        :return: None
        """
        google_speech_env_var = g_config.get_value('SpeechRecognition', 'GoogleCredentials_EnvVarName')
        if os.environ.get(google_speech_env_var) is None:
            os.environ[google_speech_env_var] = g_config.get_value('SpeechRecognition',
                                                                   'GoogleCredentials_FilePath')

    def __ensure_bucket_availability(self):
        """
        Ensures the relevant bucket is available on Google Storage.
        :return: None
        """
        bucket_name = g_config.get_value('SpeechRecognition', 'GoogleStorage_BucketName')
        if bucket_name is None:
            raise ValueError('Key not found in config file: SpeechRecognition::GoogleStorage_BucketName')

        storage_client = storage.Client()
        if storage_client.lookup_bucket(bucket_name) is None:
            # Create the new bucket
            storage_client.create_bucket(bucket_name)


class BDAGoogleStorageUploadAbstractBase(GoogleStorageBase):
    ####################
    # Private members
    __session_id = None
    __bucket_name = None
    __blob_path = None
    ####################
    # Protected members
    _path_to_file = None
    _working_dir = None
    ####################

    def __init__(self, path_to_file):
        """
        Constructor
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__()
        self.__initialization(path_to_file)

    def __del__(self):
        """
        Destructor
        """
        self.__clean_up()

    @abstractmethod
    def upload_file(self):
        pass

    def _upload_blob(self, path_to_file):
        """
        Uploads the audio file to the appropriate bucket on Google Storage.
        :return:                   None
        """
        storage_client = storage.Client()

        bucket = storage_client.get_bucket(self.__bucket_name)
        blob = bucket.blob(self.__blob_path)
        blob.upload_from_filename(path_to_file)

        return self.__bucket_name, self.__blob_path

    def __initialization(self, path_to_file):
        """
        Validation, clean-up and initialization
        :param path_to_file: Absolute path to video file.
        :return:             None
        :raises              ValueError in case validation fails.
        """
        if not os.path.isfile(path_to_file):
            raise ValueError('File not found.')

        idx_last_slash = path_to_file.rfind('/')
        if idx_last_slash < 0:
            raise ValueError('Invalid file path specified: %s' % path_to_file)

        self.__bucket_name = g_config.get_value('SpeechRecognition', 'GoogleStorage_BucketName')
        if self.__bucket_name is None:
            raise ValueError('Key not found in config file: SpeechRecognition::GoogleStorage_BucketName')

        self.__clean_up()
        self._path_to_file = path_to_file

        # Session ID --> MACAddress_TimestampInMS
        self.__session_id = str(getnode()) + '_' + str(int(time.time() * 1000))
        self.__blob_path = self.__session_id + '/audioFile.flac'
        self._working_dir = path_to_file[: idx_last_slash + 1] + self.__session_id + '/'
        if not os.path.exists(self._working_dir):
            os.makedirs(self._working_dir)

    def __clean_up(self):
        """
        Delete working with its contents.
        :return: None
        """
        if self._working_dir is not None and os.path.isdir(self._working_dir):
            shutil.rmtree(self._working_dir)


class BDAGoogleStorageUpload(BDAGoogleStorageUploadAbstractBase):
    def __init__(self, path_to_file):
        """
        Constructor
        :param path_to_file: Absolute path to file.
        """
        super().__init__(path_to_file)

    def upload_file(self):
        """
        Upload file to Google Storage platform, without FLAC file format validation.
        :return: (bucket_name, blob_path)
        """
        return self._upload_blob(self._path_to_file)

    def upload_file_debug(self):
        """
        Upload file to Google Storage platform, with FLAC file format validation.
        :return: (bucket_name, blob_path)
        """
        is_valid, result = BDAVideoToAudio.verify_audio_flac_format(self._path_to_file)
        if is_valid is False:
            raise ValueError('Input audio file does not meet the FLAC format requirements.')

        return self._upload_blob(self._path_to_file)


class BDAGoogleStorageConvertUpload(BDAGoogleStorageUploadAbstractBase):
    def __init__(self, path_to_file):
        """
        Constructor
        :param path_to_file: Absolute path to file.
        """
        super().__init__(path_to_file)

    def upload_file(self):
        """
        Convert media file to FLAC and upload to Google Storage platform.
        :return: (bucket_name, blob_path)
        """
        path_to_flac_file = BDAVideoToAudio.video_to_audio(self._path_to_file, self._working_dir, 48000, 'flac')
        return self._upload_blob(path_to_flac_file)


class BDAGoogleStorageConsume(GoogleStorageBase):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def transcribe_file(self, bucket_name, blob_path):
        """
        Transcribe file on Google Storage. Deletes file when transcription is complete.
        :param bucket_name: Bucket name on Google Storage
        :param blob_path:   Path to FLAC file on Google Storage
        :return:            Transcribed string
        """
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri='gs://' + bucket_name + '/' + blob_path)

        config = types.RecognitionConfig(
            encoding="FLAC",
            sample_rate_hertz=48000,
            language_code='en-US')

        operation = client.long_running_recognize(config, audio)
        transcription_results = operation.result()
        self.__delete_blob(bucket_name, blob_path)

        transcribed_result = ''
        for idx in range(len(transcription_results.results)):
            if len(transcription_results.results[idx].alternatives) > 0:
                transcribed_result += ' '
                transcribed_result += transcription_results.results[idx].alternatives[0].transcript

        return transcribed_result

    def __delete_blob(self, bucket_name, blob_path):
        """
        Deletes the FLAC file from the bucket on Google Storage.
        :return: None
        """
        storage_client = storage.Client()

        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_path)
        if blob.exists():
            blob.delete()


############################################################
# path_to_file_invalid = '/home/niki/Desktop/deleteMe/FFmpy/aaa/JohnOliver.mp4.Stereo.flac'
# path_to_file_valid = '/home/niki/Desktop/deleteMe/FFmpy/aaa/000_split_JohnOliver.mp4.flac'
#
# try:
#     x = BDAGoogleStorageUpload(path_to_file_valid)
#     bucket_name, path_to_blob = x.upload_file()
#     print(bucket_name)
#     print(path_to_blob)
#
# except ValueError as e:
#     print(str(e))
############################################################
# path_to_video_file = '/home/niki/Desktop/deleteMe/FFmpy/aaa/JohnOliver.mp4'
# try:
#     x = BDAGoogleStorageConvertUpload(path_to_video_file)
#     bucket_name, path_to_blob = x.upload_file()
#     print(bucket_name)
#     print(path_to_blob)
#
# except ValueError as e:
#     print(str(e))
############################################################
# bucket_name = 'big_data_assignment_bucket'
# blob_path = '44883553471107_1522595041002/audioFile.flac'
# try:
#     x = BDAGoogleStorageConsume()
#     result = x.transcribe_file(bucket_name, blob_path)
#     print(result)
#
# except ValueError as e:
#     print(str(e))
############################################################
