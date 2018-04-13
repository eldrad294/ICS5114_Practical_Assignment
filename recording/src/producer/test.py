from recording.src.speech_recognition.BDAGoogleStorage import BDAGoogleStorageUpload

path_to_file_invalid = '/home/niki/Desktop/deleteMe/FFmpy/aaa/JohnOliver.mp4.Stereo.flac'
#path_to_file_valid = '/home/niki/Desktop/deleteMe/FFmpy/aaa/000_split_JohnOliver.mp4.flac'
path_to_file_valid = "/home/gabriel/ICS5114_Practical_Assignment/recording/src/video_buffer/8796748372106_1523605924000/bobross_youtube_201841395132.flac.flac"

try:
    x = BDAGoogleStorageUpload(path_to_file_valid)
    bucket_name, path_to_blob = x.upload_file()
    print(bucket_name)
    print(path_to_blob)

except ValueError as e:
    print(str(e))