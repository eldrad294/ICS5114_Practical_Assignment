#!/bin/bash

arrayRunningVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=running --format={{.Name}} | grep 'azure-'))
arrayStoppedVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=stopped --format={{.Name}} | grep 'azure-'))

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
            docker-machine env ${arrayStoppedVMs[$i]}
            docker-machine regenerate-certs -f ${arrayStoppedVMs[$i]}
        done
    else
        arrayUserSelection=($userSelection)

        for (( i=0; i<${#arrayUserSelection[@]}; i++ )); do
            if [[ "${arrayUserSelection[$i]}" -lt ${#arrayStoppedVMs[@]} ]]; then
                docker-machine start ${arrayStoppedVMs[${arrayUserSelection[$i]}]}
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
