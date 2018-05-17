#!/bin/bash

arrayRunningVMs=($(docker-machine ls --filter driver=$1 --filter state=running --format={{.Name}}))
arrayStoppedVMs=($(docker-machine ls --filter driver=$1 --filter state=stopped --format={{.Name}}))

printf "Running VMs:\n"
for (( i=0; i<${#arrayRunningVMs[@]}; i++ )); do
    printf "  * %s\n" ${arrayRunningVMs[$i]}
done

if [[ ${#arrayStoppedVMs[@]} -gt "0" ]]; then
    printf "\nStopped VMs:\n"
    for (( i=0; i<${#arrayStoppedVMs[@]}; i++ )); do
        printf "  $i) %s\n" ${arrayStoppedVMs[$i]}
    done

    printf "\nSelect VM index, if empty, start all: "
    read userSelection

    if [[ -z "${userSelection}" ]]; then
        docker-machine start ${arrayStoppedVMs[@]}
        for (( i=0; i<${#arrayStoppedVMs[@]}; i++ )); do
            docker-machine ssh ${arrayStoppedVMs[$i]} "tce-load -i /mnt/sda1/tce/optional/nmap.tcz"
        done
    elif [[ "${userSelection}" -lt ${#arrayStoppedVMs[@]} ]]; then
        docker-machine start ${arrayStoppedVMs[$userSelection]}
        docker-machine ssh ${arrayStoppedVMs[@]} "tce-load -i /mnt/sda1/tce/optional/nmap.tcz"
    else
        printf "Wrong input.\n"
    fi
else
    printf "No available VMs.\n"
fi
