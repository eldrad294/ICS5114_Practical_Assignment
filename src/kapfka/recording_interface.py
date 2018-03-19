#
# Module imports
from subprocess import run
import subprocess
from src.constants import path_consts as pc
import datetime
#
class RecordingInterface:
    """
    This class contains the logic required to monitor and
    record data from the varied platforms which the system
    will read from. It utilizes the Streamlink command line
    tool, to connect to a streaming URL and save it as
    video/audio locally.

    This class will operate on data pulled off the config_interface.
    """
    #
    def __init__(self, config_obj, segment_time_span=300, extension='wav', quality='worst'):
        """
        Default constructor
        :param config_obj:
        :param segment_size: Denotes the time in seconds for each recording of each segmented file
        """
        self.config_obj = config_obj
        self.segment_time_span = segment_time_span
        self.extension = extension
        self.quality = quality
        self.video_buffer_path = pc.DIR_VIDEO_BUFFER
    #
    def capture(self):
        """
        Calls a never ending loop, ensuring that each
        iteration of the loops never lasts longer as
        that stated by the segment_time_span_parameter
        :return:
        """
        #
        while True:
            try:
                print("Initiating file segmentation..")
                segmented_file_name = self.get_segmented_file_name()
                command = "streamlink -o " + \
                          self.video_buffer_path + \
                          "/" + segmented_file_name + \
                          " " + self.config_obj.get_details()['url'] + \
                          " " + self.quality
                #
                output = run(args=command,
                             timeout=self.segment_time_span,
                             shell=True)
                #
                print(command)
                if (output.returncode == 0):
                    print("File [" + segmented_file_name + "] has been shipped to [" + self.video_buffer_path + "]")
            except subprocess.TimeoutExpired as te:
                pass
            except KeyboardInterrupt:
                print("User Interrupt!")
            except Exception as e:
                print("Capture method aborted in an unhandled manner!\n")
                print(str(e))
                break
    #
    def get_segmented_file_name(self):
        """
        Returns a unique file name for segmented file
        :return:
        """
        obj = self.config_obj.get_details()
        return str(obj['channel']) + "_" + \
               str(obj['platform']) + "_" + \
               self.get_time_stamp() + \
               "." + str(self.extension)
    #
    def get_time_stamp(self):
        """
        Returns timestamp of following format:
        eg: 2018319161339
        :return:
        """
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + \
               str(currentDT.month) + \
               str(currentDT.day) + \
               str(currentDT.hour) + \
               str(currentDT.minute) + \
               str(currentDT.second)
