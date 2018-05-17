#!/bin/bash

arrayVMs=($(docker-machine ls --filter driver=virtualbox --filter state=running --format={{.Name}}))

for (( i=0; i<${#arrayVMs[@]}; i++ )); do
    containerName=""
    if [[ ${arrayVMs[$i]} = *"kafka"* ]]; then
        containerName="kafka"
    elif [[ ${arrayVMs[$i]} = *"storm"* ]]; then
        containerName="storm"
    elif [[ ${arrayVMs[$i]} = *"producer"* ]]; then
        containerName="producer"
    elif [[ ${arrayVMs[$i]} = *"neo4j"* ]]; then
        containerName="neo4j"
    fi

    printf "Stopping container: $containerName\n"
    docker-machine ssh ${arrayVMs[$i]} "docker stop $containerName" >/dev/null 2>&1
done