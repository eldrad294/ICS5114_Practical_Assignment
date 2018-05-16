#!/bin/bash

for i in `seq 1 $2`; do
    vmName=`printf virtualbox-$1-%03d $i`
    docker-machine create --driver virtualbox $vmName
done
