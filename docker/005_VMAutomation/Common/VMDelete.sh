#!/bin/bash

arrayVMs=($(docker-machine ls --filter driver=$1 --format={{.Name}}))

if [[ ${#arrayVMs[@]} -gt "0" ]]; then
  printf "VMs present:\n"
  for (( i=0; i<${#arrayVMs[@]}; i++ )); do
    printf "  $i) %s\n" ${arrayVMs[$i]}
  done

  printf "\nSelect VM index, if empty, start all: "
  read userSelection

  if [[ -z "${userSelection}" ]]; then
    docker-machine rm -y ${arrayVMs[@]}
  elif [[ "${userSelection}" -lt ${#arrayVMs[@]} ]]; then
    docker-machine rm -y ${arrayVMs[$userSelection]}
  else
    printf "Wrong input.\n"
  fi
else
  printf "No available VMs.\n"
fi
