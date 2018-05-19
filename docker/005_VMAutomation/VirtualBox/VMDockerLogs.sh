#!/bin/bash

arrayRunningVMs=($(docker-machine ls --filter driver=$1 --filter state=running --format={{.Name}}))

if [[ ${#arrayRunningVMs[@]} -gt "0" ]]; then
    printf "\nRunning VMs:\n"
    for (( i=0; i<${#arrayRunningVMs[@]}; i++ )); do
        printf "  $i) %s\n" ${arrayRunningVMs[$i]}
    done

    printf "\nSelect VM index, if empty, start all: "
    read userSelection

    if [[ "$userSelection" -lt ${#arrayRunningVMs[@]} ]]; then
        containerName=""
        if [[ ${arrayRunningVMs[$userSelection]} = *"kafka"* ]]; then
            containerName="kafka"
        elif [[ ${arrayRunningVMs[$userSelection]} = *"storm"* ]]; then
            containerName="storm"
        elif [[ ${arrayRunningVMs[$userSelection]} = *"producer"* ]]; then
            containerName="producer"
        elif [[ ${arrayRunningVMs[$userSelection]} = *"neo4j"* ]]; then
            containerName="neo4j"
        fi

        docker-machine ssh ${arrayRunningVMs[$userSelection]} "docker logs -f $containerName"
    else
        printf "Wrong input.\n"
    fi
else
    printf "No available VMs.\n"
fi
