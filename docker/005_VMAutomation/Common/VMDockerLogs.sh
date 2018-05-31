#!/bin/bash

arrayRunningVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=running --format={{.Name}}))

if [[ ${#arrayRunningVMs[@]} -gt "0" ]]; then
    printf "\nRunning VMs:\n"
    for (( i=0; i<${#arrayRunningVMs[@]}; i++ )); do
        printf "  $i) %s\n" ${arrayRunningVMs[$i]}
    done

    printf "\nSelect VM index: "
    read userSelection

    if [[ "$userSelection" -lt ${#arrayRunningVMs[@]} ]]; then
        containerName=""
        if [[ ${arrayRunningVMs[$userSelection]} = *"kafka"* ]]; then
            containerName="kafka"
        elif [[ ${arrayRunningVMs[$userSelection]} = *"storm"* ]]; then
            containerName="storm"
        elif [[ ${arrayRunningVMs[$userSelection]} = *"producer"* ]]; then
            runningContainers=($(docker-machine ssh ${arrayRunningVMs[$userSelection]} "docker ps --format={{.Names}}" | grep producer))
            printf "  Running containers:\n"
            for (( j=0; j<${#runningContainers[@]}; j++ )); do
                printf "  $j) %s\n" ${runningContainers[$j]}
            done
            printf "\nSelect container index: "
            read userContainerSelection

            if [[ "$userContainerSelection" -lt ${#runningContainers[@]} ]]; then
                containerName=${runningContainers[$userContainerSelection]}
            else
                printf "Wrong input.\n"
                exit 1
            fi
        elif [[ ${arrayRunningVMs[$userSelection]} = *"neo4j"* ]]; then
            containerName="neo4j"
        fi

        docker-machine ssh ${arrayRunningVMs[$userSelection]} "sudo docker logs -f $containerName"
    else
        printf "Wrong input.\n"
    fi
else
    printf "No available VMs.\n"
fi
