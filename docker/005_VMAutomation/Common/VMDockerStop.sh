#!/bin/bash

arrayVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=running --format={{.Name}}))

for (( i=0; i<${#arrayVMs[@]}; i++ )); do
    containerName=""
    if [[ ${arrayVMs[$i]} = *"kafka"* ]]; then
        containerName[0]="kafka"
    elif [[ ${arrayVMs[$i]} = *"storm"* ]]; then
        containerName[0]="storm"
    elif [[ ${arrayVMs[$i]} = *"producer"* ]]; then
        containerName=($(docker-machine ssh ${arrayVMs[$i]} "sudo docker ps --format={{.Names}}" | grep producer))
    elif [[ ${arrayVMs[$i]} = *"neo4j"* ]]; then
        containerName[0]="neo4j"
    fi

    for (( j=0; j<${#containerName[@]}; j++ )); do
        printf "Stopping container: ${containerName[$j]}\n"
        docker-machine ssh ${arrayVMs[$i]} "sudo docker stop ${containerName[$j]}" >/dev/null 2>&1
    done
done