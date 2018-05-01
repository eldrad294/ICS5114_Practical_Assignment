#!/bin/bash

cd /root/src/ICS5114_Practical_Assignment
git pull
cd
source ~/.bashrc

/usr/bin/python3 /root/src/ICS5114_Practical_Assignment/recording/src/producer/producer_runner.py
