#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Needs root priveleges.."
    exit
fi

apt-get -y install ffmpeg

# Python packages
pip install ffmpy
pip install configparser
pip install --upgrade google-cloud-speech
pip install --upgrade google-cloud-storage