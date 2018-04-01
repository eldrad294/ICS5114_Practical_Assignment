import os
import datetime
from subprocess import Popen, PIPE
from ffmpy import FFmpeg


class BDAVideoToAudio:
    @staticmethod
    def split_video_to_audio_files(path_to_video_file, output_directory, freq, sec_per_file=50, audio_format='FLAC'):
        # 0. Results returned to caller
        result_files = list()

        # 1. Input validation
        BDAVideoToAudio.__validation(path_to_video_file, output_directory)
        if output_directory[len(output_directory) - 1] is not '/':
            output_directory += '/'

        # 2. Split video file
        split_video_files = BDAVideoToAudio.__split_video_file(path_to_video_file, output_directory, sec_per_file)

        # 3. Video split to audio
        for curr_split_video in split_video_files:
            path_to_split_file = output_directory + curr_split_video
            result_files.append(BDAVideoToAudio.video_to_audio(path_to_split_file, output_directory, freq, audio_format))
            os.remove(path_to_split_file)

        return result_files

    @staticmethod
    def video_to_audio(path_to_video_file, output_directory, freq, audio_format='FLAC'):
        output_file = path_to_video_file[path_to_video_file.rfind('/') + 1:] + '.' + audio_format
        output_file = output_directory + output_file

        output_cmd = '-ac 1 -ar ' + str(freq)

        ff = FFmpeg(
            inputs={path_to_video_file: None},
            outputs={output_file: output_cmd},
            global_options='-loglevel quiet -y'
        )

        ff.run()

        return output_file

    @staticmethod
    def verify_audio_flac_format(path_to_file):
        is_valid = True

        if not os.path.isfile(path_to_file):
            raise ValueError('File not found.')

        process = Popen([
            'ffprobe',
            '-i',            path_to_file,
            '-show_entries', 'stream=codec_name,channels,sample_rate',
            '-print_format', 'csv',
            '-hide_banner'
        ], stdout=PIPE)

        (output, err) = process.communicate()
        file_info = None
        if process.wait() == 0:
            str_out = str(output).replace('\\n', '')[1:]
            str_out = str_out.replace("'", '')

            file_info = str_out.split(',')

            if len(file_info) == 4:
                is_valid &= file_info[0] == 'stream'
                is_valid &= file_info[1] == 'flac'
                is_valid &= file_info[2] == '48000'
                is_valid &= file_info[3] == '1'
            else:
                is_valid = False
                file_info = None
        else:
            raise ValueError('ffprobe failed.')

        return is_valid, file_info

    @staticmethod
    def __split_video_file(path_to_video_file, output_directory, sec_per_file):
        output_file = '%03d_split_' + path_to_video_file[path_to_video_file.rfind('/') + 1:]
        output_file = output_directory + output_file

        file_duration = str(datetime.timedelta(seconds=sec_per_file))
        out_list = output_directory + 'out.list'
        out_list_cmd = ' -segment_list ' + out_list

        ff = FFmpeg(
            inputs={path_to_video_file: None},
            outputs={output_file: '-c copy -f segment -segment_time ' + file_duration + out_list_cmd},
            global_options='-loglevel quiet -y'
        )

        ff.run()

        with open(out_list) as f:
            split_file_names = f.readlines()

        split_file_names = [x.strip() for x in split_file_names]
        os.remove(out_list)

        return split_file_names

    @staticmethod
    def __validation(path_to_video_file, output_directory):
        if not os.path.isfile(path_to_video_file):
            raise ValueError('File not found.')
        if not os.path.isdir(output_directory):
            raise ValueError('Directory not found.')

# # Usage example:
# inFile = '/home/niki/Desktop/deleteMe/FFmpy/aaa/JohnOliver.mp4'
# outDir = '/home/niki/Desktop/deleteMe/FFmpy/aaa/'
#
# result = BDAVideoToAudio.split_video_to_audio_files(inFile, outDir, 48000)
# print(result)
# --> ['/home/niki/Desktop/deleteMe/FFmpy/aaa/000_split_JohnOliver.mp4.FLAC',
#      '/home/niki/Desktop/deleteMe/FFmpy/aaa/001_split_JohnOliver.mp4.FLAC',
#      '/home/niki/Desktop/deleteMe/FFmpy/aaa/002_split_JohnOliver.mp4.FLAC']
#
# result = BDAVideoToAudio.video_to_audio(inFile, outDir, 48000)
# print(result)
# --> /home/niki/Desktop/deleteMe/FFmpy/aaa/JohnOliver.mp4.FLAC
#
# result = BDAVideoToAudio.video_to_audio(inFile, outDir, 16000, 'WAV')
# print(result)
# --> /home/niki/Desktop/deleteMe/FFmpy/aaa/JohnOliver.mp4.WAV
