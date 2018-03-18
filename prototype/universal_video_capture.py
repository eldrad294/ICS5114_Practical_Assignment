from urllib.request import urlopen
import time
#
def record_video():
    print("Recording video...")
    response = urlopen("https://www.youtube.com/8f7b279c-1461-4bbe-8288-8b7db0d94f4f")
    filename = "yt.mp3"
    f = open(filename, 'wb')

    video_file_size_start = 0
    video_file_size_end = 1024 * 1024 * 1024 * 100000  # end in 10 mb
    block_size = 1024

    while True:
        try:
            buffer = response.read(block_size)
            print(buffer)
            if not buffer:
                break
            video_file_size_start += len(buffer)
            if video_file_size_start > video_file_size_end:
                break
            f.write(buffer)

        except Exception as e:
            print(str(e))
    f.close()