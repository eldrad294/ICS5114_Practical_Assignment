#!/bin/bash

arrayRunningVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=running --format={{.Name}}))
arrayStoppedVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=stopped --format={{.Name}}))

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

    if [[ -z "$userSelection" ]]; then
        docker-machine start ${arrayStoppedVMs[@]}
        for (( i=0; i<${#arrayStoppedVMs[@]}; i++ )); do
            docker-machine ssh ${arrayStoppedVMs[$i]} "tce-load -i /mnt/sda1/tce/optional/nmap.tcz"
            docker-machine env ${arrayStoppedVMs[$i]}
            docker-machine regenerate-certs -f ${arrayStoppedVMs[$i]}
        done
    else
        arrayUserSelection=($userSelection)
        for (( i=0; i<${#arrayUserSelection[@]}; i++ )); do
            if [[ "${arrayUserSelection[$i]}" -lt ${#arrayStoppedVMs[@]} ]]; then
                docker-machine start ${arrayStoppedVMs[${arrayUserSelection[$i]}]}
                docker-machine ssh ${arrayStoppedVMs[${arrayUserSelection[$i]}]} "tce-load -i /mnt/sda1/tce/optional/nmap.tcz"
                docker-machine env ${arrayStoppedVMs[${arrayUserSelection[$i]}]}
                docker-machine regenerate-certs -f ${arrayStoppedVMs[${arrayUserSelection[$i]}]}
            else
                printf "Wrong input --> ${arrayUserSelection[$i]}\n"
            fi
        done
    fi
else
    printf "No available VMs.\n"
fi
