#!/bin/bash

# Adapted from: https://stackoverflow.com/a/14203146

PrintHelp() 
{
    printf "\n***************************************************************************************\n"
    printf "main.sh [CMD] [OPTIONS]\n\n"
    printf "Example:\n>> main.sh list -e remote\n"

    printf "\nCMD:\n----\n"
    printf "  * list:              List all VMs for a given environment.\n"
    printf "  * start:             Start VM/s for a given environment.\n"
    printf "  * stop:              Stop VM/s for a given environment.\n"
    printf "  * create:            Create VM/s for a given environment.\n"
    printf "  * delete:            Delete VM/s for a given environment.\n"

    printf "\nOPTIONS:\n--------\n"
    printf "  * -e|--environment:  Environment where the command should be executed.\n"
    printf "                       [local|remote]\n"

    printf "\n***************************************************************************************\n"
}

cmd=$1
shift

POSITIONAL=()
while [[ $# -gt 0 ]]; do
key="$1"
case $key in
    -e|--environment)
    environment="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    PrintHelp
    exit 1
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

case $cmd in
    list)
    if [[ $environment == "local" ]]; then
        source Common/VMList.sh "virtualbox"
    elif [[ $environment == "remote" ]]; then
        source Common/VMList.sh "azure"
    else
        PrintHelp
        exit 1
    fi
    ;;

    start)
    if [[ $environment == "local" ]]; then
        source Common/VMStart.sh "virtualbox"
    elif [[ $environment == "remote" ]]; then
        source Common/VMStart.sh "azure"
    else
        PrintHelp
        exit 1
    fi
    ;;

    stop)
    if [[ $environment == "local" ]]; then
        source Common/VMStop.sh "virtualbox"
    elif [[ $environment == "remote" ]]; then
        source Common/VMStop.sh "azure"
    else
        PrintHelp
        exit 1
    fi
    ;;

    create)
    PrintHelp
    exit 1

    if [[ $environment == "local" ]]; then
        source Common/VMCreate.sh "virtualbox"
    elif [[ $environment == "remote" ]]; then
        source Common/VMCreate.sh "azure"
    else
        PrintHelp
        exit 1
    fi
    ;;

    delete)
    if [[ $environment == "local" ]]; then
        source Common/VMDelete.sh "virtualbox"
    elif [[ $environment == "remote" ]]; then
        source Common/VMDelete.sh "azure"
    else
        PrintHelp
        exit 1
    fi
    ;;

    *)    # unknown option
    PrintHelp
    ;;
esac
