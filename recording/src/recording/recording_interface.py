#
# Module imports
from subprocess import run
from recording.src.constants import path_consts as pc
import datetime, subprocess
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
    def __init__(self, config_obj, segment_time_span=300, extension='wav', quality='worst', video_buffer_path=pc.DIR_VIDEO_BUFFER):
        """
        Default constructor
        :param config_obj:
        :param segment_size: Denotes the time in seconds for each recording of each segmented file
        """
        self.config_obj = config_obj
        self.segment_time_span = segment_time_span
        self.extension = extension
        self.quality = quality
        self.video_buffer_path = video_buffer_path
    #
    def capture_and_save_indefinetly(self):
        """
        Calls a never ending loop on the capture_and_save method
        :return:
        """
        #
        while True:
            self.capture_and_save()
    #
    def capture_and_save(self):
        """
        Recording logic, using the streamlink CLI tool.
        All captured footage is saved to disk. Footage
        time is dicated by the segment_time_span_parameter
        parameter
        :return:
        """
        print("Initiating file segmentation..")
        segmented_file_name = self.get_segmented_file_name()
        try:
            output = self.stream_link_wrapper(segmented_file_name)
            #
            if (output.returncode == 0):
                print("File [" + segmented_file_name + "] has been shipped to [" + self.video_buffer_path + "]")
        except subprocess.TimeoutExpired:
            pass
        except KeyboardInterrupt:
            print("User Interrupt!")
        except Exception as e:
            print("Capture method aborted in an unhandled manner!\n")
            print(str(e))
            exit(1)
    #
    def capture_and_return(self):
        """
        Similar to the capture_and_save method, but returns the
        recorded file path.
        :return:
        """
        print("Initiating file segmentation..")
        segmented_file_name = self.get_segmented_file_name()
        try:
            output = self.stream_link_wrapper(segmented_file_name)
            #
            if (output.returncode == 0):
                print("File [" + segmented_file_name + "] has been shipped to [" + self.video_buffer_path + "]")
                return self.video_buffer_path + "/" + segmented_file_name
        except subprocess.TimeoutExpired:
            return self.video_buffer_path + "/" + segmented_file_name
        except KeyboardInterrupt:
            print("User Interrupt!")
            return None
        except Exception as e:
            print("Capture method aborted in an unhandled manner!\n")
            print(str(e))
            return None
    #
    def stream_link_wrapper(self, segmented_file_name):
        """
        Method which encapsulates the streamlink tools
        :return:
        """
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
        return output
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
    #
    def get_video(self, video_path):
        """
        NB: Beware using this method on large files!
        This function will copy the file content as
        binary data into memory.
        :param video_path:
        :return:
        """
        #
        # Opening for [r]eading as [b]inary
        with open(video_path, "rb") as file:
            data = file.read()
            file.close()
        return data
