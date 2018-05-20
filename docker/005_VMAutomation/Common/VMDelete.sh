#!/bin/bash

arrayVMs=($(docker-machine ls -t 60 --filter driver=$1 --format={{.Name}}))

if [[ ${#arrayVMs[@]} -gt "0" ]]; then
    printf "VMs present:\n"
    for (( i=0; i<${#arrayVMs[@]}; i++ )); do
        printf "  $i) %s\n" ${arrayVMs[$i]}
    done

    printf "\nSelect VM index, if empty, delete all: "
    read userSelection

    if [[ -z "$userSelection" ]]; then
        docker-machine rm -y ${arrayVMs[@]}
    else
        arrayUserSelection=($userSelection)
        for (( i=0; i<${#arrayUserSelection[@]}; i++ )); do
            if [[ "${arrayUserSelection[$i]}" -lt ${#arrayVMs[@]} ]]; then
                docker-machine rm -y ${arrayVMs[${arrayUserSelection[$i]}]}
            else
                printf "Wrong input --> ${arrayUserSelection[$i]}\n"
            fi
        done
    fi
else
    printf "No available VMs.\n"
fi
