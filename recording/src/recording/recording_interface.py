import shlex
import datetime, subprocess, re, math
from recording.src.constants import path_consts as pc
from pytube import YouTube


class RecordingInterface:
    """
    This class contains the logic required to monitor and record data from the varied platforms which the system will
    read from. It has 2 modes to interpret and record video data:

    1) Utilizes ffmpeg to split a video into several smaller ones. This functionality is reserved for pre-recorded
    footage which is downloaded, segmented locally into smaller chunks, to be eventually pushed down the pipeline.

    2) Utilizes the Streamlink command line tool, to connect to a streaming online source and saves it as segmented
    videos/audio locally.

    This class will operate on data pulled off the config_interface.
    """
    def __init__(self, config_obj, segment_time_span=300, extension='wav', quality='worst',
                 video_buffer_path=pc.DIR_VIDEO_BUFFER):
        """
        Default constructor

        :param config_obj:         A class structure used to contain information acquired from the input_channels.json config file
        :param segment_time_span:  Denotes the time in seconds for each recording of each segmented file
        :param extension:          Video file format to save footage in
        :param quality:            Recording quality to capture footage with
        :param video_buffer_path:  Local path to save file to disk during recording
        """
        self.config_obj = config_obj
        self.segment_time_span = segment_time_span
        self.extension = extension
        self.quality = quality
        self.video_buffer_path = video_buffer_path

    def capture_and_save_indefinetly(self):
        """
        Calls an infinite loop on the capture_and_save method
        :return: None
        """
        while True:
            self.capture_and_save()

    def capture_and_save(self):
        """
        Recording logic, using the streamlink CLI tool. All captured footage is saved to disk. Footage time is
        determined by the segment_time_span_parameter parameter
        :return: None
        """
        print("Initiating file segmentation..")
        segmented_file_name = self.get_segmented_file_name()
        try:
            output = self.stream_link_wrapper(segmented_file_name)
            if output.returncode == 0:
                print("File [" + segmented_file_name + "] has been shipped to [" + self.video_buffer_path + "]")
        except subprocess.TimeoutExpired:
            pass
        except KeyboardInterrupt:
            print("User Interrupt!")
        except Exception as e:
            print("Capture method aborted in an unhandled manner!\n")
            print(str(e))
            exit(1)

    def capture_and_return(self):
        """
        Similar to the capture_and_save method, but returns the recorded file path.
        :return: Path to file
        """
        print("Initiating file segmentation..")
        segmented_file_name = self.get_segmented_file_name()
        try:
            proc = self.stream_link_wrapper(segmented_file_name)

            # The spawned process does not terminate, therefore it is expected that a subprocess.TimeoutExpired
            # exception is raised.
            proc.wait(self.segment_time_span)
            print('Unreachable code.')
            return None

        except subprocess.TimeoutExpired:
            print("File [" + segmented_file_name + "] has been shipped to [" + self.video_buffer_path + "]")
            proc.terminate()
            return self.video_buffer_path + "/" + segmented_file_name

        except KeyboardInterrupt:
            print("User Interrupt!")
            return None

        except Exception as e:
            print("Capture method aborted in an unhandled manner!\n")
            print(str(e))
            return None

    def stream_link_wrapper(self, segmented_file_name):
        """
        Method which encapsulates the streamlink tools
        :param segmented_file_name: Segment file name
        :return:                    Handle to the spawned OS process
        """
        command = "streamlink -o " + \
                  self.video_buffer_path + \
                  "/" + segmented_file_name + \
                  " " + self.config_obj.get_details()['src'][0] + \
                  " " + self.quality
        return subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

    def get_segmented_file_name(self):
        """
        :return: Returns a unique file name for segmented file
        """
        obj = self.config_obj.get_details()
        return str(obj['channel']) + "_" + \
               str(obj['platform']) + "_" + \
               self.get_time_stamp() + \
               "." + str(self.extension)

    def get_time_stamp(self):
        """
        :return: Returns timestamp of the format: 2018319161339
        """
        currentDT = datetime.datetime.now()
        return str(currentDT.year) + \
               str(currentDT.month) + \
               str(currentDT.day) + \
               str(currentDT.hour) + \
               str(currentDT.minute) + \
               str(currentDT.second)

    def get_video(self, video_path):
        """
        This function will copy the file content as binary data into memory.
        NB: Beware using this method on large files!
        :param video_path: Path to video file
        :return:           File content representation in memory
        """
        # Opening for [r]eading as [b]inary
        with open(video_path, "rb") as file:
            data = file.read()
            file.close()
        return data

    def download_and_segment(self):
        """
        Wrapper function for downloading and segmenting of youtube videos
        :return:
        """
        local_video_paths = self.__download_videos()
        return self.__segment_local_videos(local_video_paths=local_video_paths)

    def __clean_downloaded_videos(self, title_name):
        """
        Cleans video name from illegal characters
        :param title_name: Video title
        :return:           Cleaned version of the video title
        """
        illegal_characters = ('"', "'", "\\", "/", ",", ".", "&", "%", " ", "+","-","#","$","!","?",":","(",")","^","@","~","*","<",">")
        return_string = []
        for char in str(title_name):
            if char not in illegal_characters:
                return_string.append(char)
        return "".join(return_string)

    def __download_videos(self):
        """
        Downloads videos from youtube src
        :return: List of paths to the downloaded video files
        """
        local_paths = []
        print("Initiating YouTube Connection..")
        for yt_src in self.config_obj.get_details()['src']:
            yt = YouTube(yt_src)
            stream = yt.streams.filter(resolution='144p').first()
            print("Downloading content at " + pc.PARENT_DIR + "/src/video_buffer..")
            title = self.__clean_downloaded_videos(yt.title)
            stream.download(output_path=pc.PARENT_DIR+"/src/video_buffer/", filename=title)
            local_paths.append(pc.PARENT_DIR + "/src/video_buffer/" + title + ".3gpp")
        return local_paths

    def __segment_local_videos(self, local_video_paths):
        """
        Segments a number local videos
        :param local_video_paths: File path where the content was downloaded
        :return:                  List of video file paths
        """
        video_paths = []
        length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
        re_length = re.compile(length_regexp)

        print("Initiating file segmentation..")
        for i, file_path in enumerate(local_video_paths):
            segmented_file_name = file_path
            print("Segmenting [" + segmented_file_name + "]")

            if self.segment_time_span <= 0:
                print("Split length can't be 0")
                raise SystemExit

            cmd = "ffmpeg -i '" + segmented_file_name + "' 2>&1 | grep Duration"
            output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE ).stdout.read()

            matches = re_length.search(str(output))
            if matches:
                video_length = int(matches.group(1)) * 3600 + \
                               int(matches.group(2)) * 60 + \
                               int(matches.group(3))
                print("Video length in seconds: " + str(video_length))
            else:
                print("Can't determine video length for [" + segmented_file_name + "]")
                raise SystemExit

            split_count = math.ceil(video_length / float(self.segment_time_span))
            if split_count == 1:
                print("Video length is less then the target split length.")
                raise SystemExit

            split_cmd = "ffmpeg -i '" + segmented_file_name + "' -vcodec copy "

            for n in range(int(split_count)):
                split_str = ""
                if n == 0:
                    split_start = 0
                else:
                    split_start = self.segment_time_span * n

                # Ensures a unique file_name for the segmented file on disk
                segmented_file_name = pc.PARENT_DIR + "/src/video_buffer/" + str(i) + str(n) + "_" + \
                                      self.get_segmented_file_name()
                split_str += " -ss " + str(split_start) + " -t " + str(self.segment_time_span) + \
                             " '" + segmented_file_name + "'"
                try:
                    print("About to run: " + split_cmd + split_str)
                    output = subprocess.Popen(split_cmd + split_str, shell=True, stdout=subprocess.PIPE).stdout.read()
                    video_paths.append(segmented_file_name)
                except Exception as e:
                    print("Exception caught during local video segmentation [" + str(e) + "]")
        return video_paths
