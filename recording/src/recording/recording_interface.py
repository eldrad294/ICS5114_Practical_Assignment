#
# Module imports
from subprocess import run
from recording.src.constants import path_consts as pc
import datetime, subprocess, re, math
from optparse import OptionParser

#
class RecordingInterface:
    """
    This class contains the logic required to monitor and
    record data from the varied platforms which the system
    will read from. It has 2 modes to interpret and record
    video data:

    1) Utilizes ffmpeg to split a video into several smaller
    ones.

    2) Utilizes the Streamlink command line
    tool, to connect to a streaming online source
    and saves it as segmented videos/audio locally.

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
                  " " + self.config_obj.get_details()['src'] + \
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
    ########################################
    ########################################
    #
    def segment_local_video(self):
        """
        Segments a local video
        :param filename:
        :param split_length: Defined in seconds
        :return:
        """
        length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
        re_length = re.compile(length_regexp)
        #
        print("Initiating file segmentation..")
        segmented_file_name = self.config_obj.get_details()['src']
        #
        if self.segment_time_span <= 0:
            print("Split length can't be 0")
            raise SystemExit
        #
        output = subprocess.Popen("ffmpeg -i " + segmented_file_name + " 2>&1 | grep Duration",
                                  shell=True,
                                  stdout=subprocess.PIPE
                                  ).stdout.read()
        #print(output)
        matches = re_length.search(str(output))
        if matches:
            video_length = int(matches.group(1)) * 3600 + \
                           int(matches.group(2)) * 60 + \
                           int(matches.group(3))
            print("Video length in seconds: " + str(video_length))
        else:
            print("Can't determine video length for [" + segmented_file_name + "]")
            raise SystemExit
        #
        split_count = math.ceil(video_length / float(self.segment_time_span))
        if (split_count == 1):
            print("Video length is less then the target split length.")
            raise SystemExit
        #
        split_cmd = "ffmpeg -i '" + segmented_file_name + "' -vcodec copy "
        video_paths = []
        for n in range(int(split_count)):
            split_str = ""
            if n == 0:
                split_start = 0
            else:
                split_start = self.segment_time_span * n
            #
            segmented_file_name = self.video_buffer_path + "/" + str(n) + "_" + self.get_segmented_file_name()
            split_str += " -ss " + str(split_start) + " -t " + str(self.segment_time_span) + \
                         " '" + segmented_file_name + "'"
            print("About to run: " + split_cmd + split_str)
            output = subprocess.Popen(split_cmd + split_str, shell=True, stdout=subprocess.PIPE).stdout.read()
            video_paths.append(segmented_file_name)
        return video_paths