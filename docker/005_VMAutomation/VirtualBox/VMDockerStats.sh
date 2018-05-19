#!/bin/bash

arrayRunningVMs=($(docker-machine ls --filter driver=$1 --filter state=running --format={{.Name}}))

cmdArray=()

for (( i=0; i<${#arrayRunningVMs[@]}; i++ )); do
    if [[ ${arrayRunningVMs[$i]} = *"kafka"* ]]; then
        cmdArray[$i]="docker-machine ssh ${arrayRunningVMs[$i]} 'docker stats kafka --no-stream'"
    elif [[ ${arrayRunningVMs[$i]} = *"storm"* ]]; then
        cmdArray[$i]="docker-machine ssh ${arrayRunningVMs[$i]} 'docker stats storm --no-stream'"
    elif [[ ${arrayRunningVMs[$i]} = *"producer"* ]]; then
        cmdArray[$i]="docker-machine ssh ${arrayRunningVMs[$i]} 'docker stats producer --no-stream'"
    elif [[ ${arrayRunningVMs[$i]} = *"neo4j"* ]]; then
        cmdArray[$i]="docker-machine ssh ${arrayRunningVMs[$i]} 'docker stats neo4j --no-stream'"
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
