#!/usr/bin/python

# # # # # # # # # # # # # # # # # # # #
#                                     #
# Script was made by Dennis           #
# http://stefansundin.com/blog/452    #
# http://pastebin.com/8cw9LHFg        #
#                                     #
# # # # # # # # # # # # # # # # # # # #
from urllib.request import urlopen
import os, re

datadir = '/tmp/'
# this url has to be obtained by httpfox
playlist = 'https://www.youtube.com/watch?v=rFDF99gVFMg'

def recrod_video():
    for seq in range(0, 100000):
        print("[+] Downloading playlist for seq %s..." % (seq))
        # skip if already exists
        if os.path.isfile(datadir + str(seq) + ".done"):
            print("[+] Sequence %s already done!" % (seq))
            continue
        response = urlopen(playlist + str(seq))
        html = response.read()
        for line in html:
            if line.startswith("http://"):
                seq = re.search('/sq/(\d+)/file/', line).group(1)
                print("[+] Downloading video for sequence %s..." % (seq))

                # skip if already exists
                if os.path.isfile(datadir + str(seq) + ".done"):
                    print("[+] Sequence %s already done!" % (seq))
                    continue

                response = urlopen(line)
                stream = response.read()
                f = open(datadir + str(seq) + '.asf', 'w')
                f.write(stream)
                f.close()
                f = open(datadir + str(seq) + ".done", 'w')
                f.write("")
                f.close()

    # joining stream togeather in losless manner
    # https://trac.ffmpeg.org/wiki/How%20to%20concatenate%20(join,%20merge)%20media%20files