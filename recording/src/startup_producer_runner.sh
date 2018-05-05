#!/bin/bash

cd /root/src/ICS5114_Practical_Assignment
git pull

/usr/bin/python3 -u /root/src/ICS5114_Practical_Assignment/recording/src/producer/producer_runner.py > /root/producer_runner.log
