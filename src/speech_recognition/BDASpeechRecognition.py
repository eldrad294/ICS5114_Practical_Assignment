import io
import os
import time
import shutil
from abc import ABC, abstractmethod
from subprocess import Popen, PIPE

from src.coding_framework.BDATimer import BDATimer
from coding_framework.BDAConfigParser import g_config
from src.speech_recognition.BDAVideoAudioUtilities import *

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud import storage
from google.cloud.speech import enums
from google.cloud.speech import types


# Class hierarchy
# ---------------
#                                          +---------------------------------+
#                                          |   BDASpeechRecognitionAbstract  |
#                                          +---------------+-----------------+
#                                                          |
#                                                          |
#                         +--------------------------------+--------------------------------+
#                         |                                                                 |
#                         |                                                                 |
#          +--------------+----------------+                                                |
#          |  BDAGoogleSpeechAbstractBase  |                                                |
#          +--------------+----------------+                                                |
#                         |                                                                 |
#                         |                                                                 |
#            +------------+----------------+                                                |
#            |                             |                                                |
#            |                             |                                                |
# +----------+-----------+      +----------+---------------+                   +------------+-------------+
# |  BDAGoogleSpeechAPI  |      |  BDAGoogleSpeechStorage  |                   |  BDASphinxSpeechLibrary  |
# +----------------------+      +--------------------------+                   +--------------------------+


class BDASpeechRecognitionAbstract(ABC):
    """
    Abstract base class for all transcribe classes.
    """
    ##########################
    # Protected members
    _path_to_video_file = None
    _working_dir = None
    _session_id = None
    _timer = None
    ##########################

    # Constructor
    def __init__(self, path_to_file):
        """
        Constructor
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__()
        self.reset_file(path_to_file)
        self._timer = BDATimer()

    def __del__(self):
        """
        Destructor
        """
        self.__clean_up()

    def reset_file(self, path_to_file):
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

        self.__clean_up()
        self._path_to_video_file = path_to_file
        self._session_id = str(int(time.time() * 1000))
        self._working_dir = path_to_file[: idx_last_slash + 1] + self._session_id + '/'
        if not os.path.exists(self._working_dir):
            os.makedirs(self._working_dir)

    def __clean_up(self):
        """
        Delete working with its contents.
        :return: None
        """
        if self._working_dir is not None and os.path.isdir(self._working_dir):
            shutil.rmtree(self._working_dir)

    @abstractmethod
    def transcribe_video_file(self):
        """
        Abstract method that transcribes the input video file into text.
        :return: Transcribed result.
        """
        pass


class BDAGoogleSpeechAbstractBase(BDASpeechRecognitionAbstract):
    """
    Abstract base class for all transcribe classes based on the Google Speech Recognition platform.
    """
    def __init__(self, path_to_file):
        """
        Constructor ensures the required Google Speech Recognition environment variable is present.
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__(path_to_file)
        self.__load_env_variables()

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
            os.environ[google_speech_env_var] = g_config.get_value('SpeechRecognition', 'GoogleCredentials_FilePath')


class BDAGoogleSpeechAPI(BDAGoogleSpeechAbstractBase):
    """
    Concrete derived class responsible for transcribing a video file solely through the Google Speech Recognition API.
    """
    def __init__(self, path_to_file):
        """
        Constructor
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__(path_to_file)

    def transcribe_video_file(self):
        """
        Base class abstract method implementation, making this a concrete class. This method is responsible for:
        1. Converting the input video file into an audio file.
        2. Splitting the audio file into shorter files that meet the Google Speech Recognition size limits.
        3. Upload and transcribe all the split audio files, through the Google platform.
        4. Aggregate and return the results to the client.
        :return: Transcribed result.
        """
        result = ''
        audio_split_files = BDAVideoToAudio.split_video_to_audio_files(self._path_to_video_file, self._working_dir, 48000)

        for curr_split in audio_split_files:
            result += ' '
            result += self.__transcribe_audio_file(curr_split)

        return result

    def __transcribe_audio_file(self, path_to_audio_file):
        """
        Transcribe audio file. This method is responsible for:
        1. Uploading the audio file to the Google platform.
        2. Issuing the transcribe command.
        3. Aggregate and return the results.
        :param path_to_audio_file: Absolute path to audio file. FLAC file format is preferred by the Google platform.
        :return: Transcribed result.
        """
        # Instantiates a client
        client = speech.SpeechClient()

        # Loads the audio into memory
        with io.open(path_to_audio_file, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding="FLAC",
            sample_rate_hertz=48000,
            language_code='en-US')

        response = client.recognize(config, audio)

        result = ''
        for idx in range(len(response.results)):
            if len(response.results[idx].alternatives) > 0:
                result += ' '
                result += response.results[idx].alternatives[0].transcript

        return result


class BDAGoogleSpeechStorage(BDAGoogleSpeechAbstractBase):
    """
    Concrete derived class responsible for transcribing a video file solely through the Google Speech Recognition API
    and the Google Storage platform.
    """
    ############################
    # Private members
    __bucket_name = 'big_data_assignment_bucket'
    __blob_path = None
    ############################

    def __init__(self, path_to_file):
        """
        Constructor. Ensures the required bucket on Google Storage is available.
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__(path_to_file)
        self.__blob_path = self._session_id + '/audioFile.flac'
        self.__ensure_bucket_availability()

    def transcribe_video_file(self):
        """
        Base class abstract method implementation, making this a concrete class. This method is responsible for:
        1. Converting the input video file into an audio file.
        2. Upload the resulting audio file to the appropriate Google Storage bucket.
        3. Transcribe the uploaded file.
        4. Delete the uploaded file from the Google Storage bucket.
        5. Aggregate and return the results to the client.
        :return: Transcribed result.
        """
        path_to_audio_file = BDAVideoToAudio.video_to_audio(self._path_to_video_file, self._working_dir, 48000)
        self.__upload_blob(path_to_audio_file)

        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri='gs://' + self.__bucket_name + '/' + self.__blob_path)
        config = types.RecognitionConfig(
            encoding="FLAC",
            sample_rate_hertz=48000,
            language_code='en-US')

        operation = client.long_running_recognize(config, audio)
        transcription_results = operation.result()
        self.__delete_blob()

        result = ''
        for idx in range(len(transcription_results.results)):
            if len(transcription_results.results[idx].alternatives) > 0:
                result += ' '
                result += transcription_results.results[idx].alternatives[0].transcript

        return result

    def __ensure_bucket_availability(self):
        """
        Ensures the relevant bucket is available on Google Storage.
        :return: None
        """
        storage_client = storage.Client()
        if storage_client.lookup_bucket(self.__bucket_name) is None:
            # Create the new bucket
            storage_client.create_bucket(self.__bucket_name)

    def __upload_blob(self, path_to_audio_file):
        """
        Uploads the audio file to the appropriate bucket on Google Storage.
        :param path_to_audio_file: Absolute path to audio file.
        :return:                   None
        """
        storage_client = storage.Client()

        bucket = storage_client.get_bucket(self.__bucket_name)
        blob = bucket.blob(self.__blob_path)
        blob.upload_from_filename(path_to_audio_file)

    def __delete_blob(self):
        """
        Deletes the audio file from the bucket on Google Storage.
        :return: None
        """
        storage_client = storage.Client()

        bucket = storage_client.get_bucket(self.__bucket_name)
        blob = bucket.blob(self.__blob_path)
        if blob.exists():
            blob.delete()


class BDASphinxSpeechLibrary(BDASpeechRecognitionAbstract):
    """
    Concrete derived class responsible for transcribing a video file through the offline application
    pocketsphinx_continuous.
    """
    ######################
    # Private members
    __sphinx_root_dir = None
    ######################

    def __init__(self, path_to_file):
        """
        Constructor
        :param path_to_file: Absolute path to video file. Tested on MP4 video format.
        """
        super().__init__(path_to_file)
        self.__sphinx_root_dir = g_config.get_value('SpeechRecognition', 'Sphinx_RootDir')

    def transcribe_video_file(self):
        """
        Base class abstract method implementation, making this a concrete class. This method is responsible for:
        1. Converting the input video file into a WAV audio file with 16000 sampling frequency.
        2. Transcribing the audio file through 'pocketsphinx_continuous' application in a separate child process.
        3. Aggregate and return the results to the client.
        :return: Transcribed result.
        """
        result = ''
        audio_file = BDAVideoToAudio.video_to_audio(self._path_to_video_file, self._working_dir, 16000, 'WAV')

        process = Popen([
            'pocketsphinx_continuous',
            '-infile', audio_file,                                      # Input WAV file
            '-hmm',    self.__sphinx_root_dir + '/en-us',               # Model
            '-lm',     self.__sphinx_root_dir + '/en-us.lm.bin',        # Language model
            '-dict',   self.__sphinx_root_dir + '/cmudict-en-us.dict',  # Language dictionary
            '-logfn',  '/dev/null'                                      # Suppress extra logging, output will only
                                                                        # contain the result
        ], stdout=PIPE)

        (output, err) = process.communicate()
        if process.wait() == 0:
            result = output

        return result


# # Usage example:
# Video file duration: 110 seconds
# path_to_video_file = '/home/niki/Desktop/deleteMe/FFmpy/JohnOliver.mp4'
#
# 48 seconds
# googleSpeechApi = BDAGoogleSpeechAPI(path_to_video_file)
# result = googleSpeechApi.transcribe_video_file()
# print(result)
#
# 72 seconds
# googleSpeechStorage = BDAGoogleSpeechStorage(path_to_video_file)
# result = googleSpeechStorage.transcribe_video_file()
# print(result)
#
# 176 seconds
# sphinxLibrary = BDASphinxSpeechLibrary(path_to_video_file)
# result = sphinxLibrary.transcribe_video_file()
# print(result)