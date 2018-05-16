#!/bin/bash

for i in `seq 1 $2`; do
    vmName=`printf virtualbox-$1-%03d $i`
    docker-machine create --driver virtualbox $vmName
    docker-machine ssh $vmName "tce-load -wi nmap"
    docker-machine ssh $vmName "docker pull $3"
done
