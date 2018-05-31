#!/bin/bash

arrayRunningVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=running --format={{.Name}}))

cmdArray=()

for (( i=0; i<${#arrayRunningVMs[@]}; i++ )); do
    if [[ ${arrayRunningVMs[$i]} = *"kafka"* ]]; then
        cmdArray+=("docker-machine ssh ${arrayRunningVMs[$i]} 'sudo docker stats kafka --no-stream'")
    elif [[ ${arrayRunningVMs[$i]} = *"storm"* ]]; then
        cmdArray+=("docker-machine ssh ${arrayRunningVMs[$i]} 'sudo docker stats storm --no-stream'")
    elif [[ ${arrayRunningVMs[$i]} = *"producer"* ]]; then
        containerName=($(docker-machine ssh ${arrayRunningVMs[$i]} "docker ps --format={{.Names}}" | grep producer))
        for (( j=0; j<${#containerName[@]}; j++ )); do
            cmdArray+=("docker-machine ssh ${arrayRunningVMs[$i]} 'sudo docker stats ${containerName[$j]} --no-stream'")
        done
    elif [[ ${arrayRunningVMs[$i]} = *"neo4j"* ]]; then
        cmdArray+=("docker-machine ssh ${arrayRunningVMs[$i]} 'sudo docker stats neo4j --no-stream'")
    fi
done

first=true
while true; do
    for (( i=0; i<${#cmdArray[@]}; i++ )); do
        if [[ $first == true ]]; then
            eval ${cmdArray[$i]}
            first=false
        else
            eval ${cmdArray[$i]} | grep 'kafka\|producer\|neo4j\|storm'
        fi
    done
done
