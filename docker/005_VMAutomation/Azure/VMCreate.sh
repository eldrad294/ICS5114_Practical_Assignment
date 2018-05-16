#!/bin/bash

for i in `seq 1 $2`; do
    vmName=`printf azure-$1-%03d $i`
    docker-machine create --driver azure    \
        --azure-open-port          80       \
        --azure-size               $4       \
        --azure-resource-group     $5       \
        --azure-ssh-user           $6       \
        --azure-location           $7       \
        --azure-subscription-id    $8       \
        $vmName
    docker-machine ssh $vmName "sudo apt-get install -y nmap"
    docker-machine ssh $vmName "sudo docker pull $3"
done
