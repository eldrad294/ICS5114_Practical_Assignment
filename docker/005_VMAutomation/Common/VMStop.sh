#!/bin/bash

arrayRunningVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=running --format={{.Name}} | grep "$1-"))
arrayStoppedVMs=($(docker-machine ls -t 60 --filter driver=$1 --filter state=stopped --format={{.Name}} | grep "$1-"))

printf "\nStopped VMs:\n"
for (( i=0; i<${#arrayStoppedVMs[@]}; i++ )); do
  printf "  * %s\n" ${arrayStoppedVMs[$i]}
done

if [[ ${#arrayRunningVMs[@]} -gt "0" ]]; then
  printf "\nRunning VMs:\n"
  for (( i=0; i<${#arrayRunningVMs[@]}; i++ )); do
    printf "  $i) %s\n" ${arrayRunningVMs[$i]}
  done

  printf "\nSelect VM index, if empty, stop all: "
  read userSelection

  if [[ -z "${userSelection}" ]]; then
    docker-machine stop ${arrayRunningVMs[@]}
  elif [[ "${userSelection}" -lt ${#arrayRunningVMs[@]} ]]; then
    docker-machine stop ${arrayRunningVMs[$userSelection]}
  else
    printf "Wrong input.\n"
  fi
else
  printf "No available VMs.\n"
fi
