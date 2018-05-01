#!/bin/bash

cd /root/src/ICS5114_Practical_Assignment
git pull

cd /root
source .bashrc

printf "\n\n\n-----------------------"
echo $PYTHONPATH
printf "-----------------------\n\n\n"

/usr/bin/python3 /root/src/ICS5114_Practical_Assignment/recording/src/producer/producer_runner.py
