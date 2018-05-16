#!/bin/bash

for i in `seq 1 $2`; do
    vmName=`printf azure-$1-%03d $i`
    docker-machine create --driver azure    \
        --azure-open-port          80       \
        --azure-size               $3       \
        --azure-resource-group     $4       \
        --azure-ssh-user           $5       \
        --azure-location           $6       \
        --azure-subscription-id    $7       \
        $vmName
done
