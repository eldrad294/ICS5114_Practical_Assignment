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
    printf "  * dockerstart:       Docker start-up sequence for a given environment.\n"
    printf "  * dockerstop:        Stop docker containers for a given environment.\n"
    printf "  * dockerstats:       Get running docker container statistics for a given environment.\n"
    printf "  * dockerlogs:        Get docker container log stream for a given environment.\n"

    printf "\nOPTIONS:\n--------\n"
    printf "  * -e|--environment:  Environment where the command should be executed.\n"
    printf "                       [local|remote]\n"
    printf "  * -s|--setupfile:    Setup file containing the VM specification in CSV format, used\n"
    printf "                       for VM creationEnvironment where the command should be executed.\n"

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

    -s|--setupfile)
    setupFile="$2"
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
    param=""
    if [[ $environment == "local" ]]; then
        param="virtualbox"
    elif [[ $environment == "remote" ]]; then
        param="azure"
    else
        PrintHelp
        exit 1
    fi

    source Common/VMList.sh $param
    ;;

    start)
    if [[ $environment == "local" ]]; then
        source VirtualBox/VMStart.sh "virtualbox"
    elif [[ $environment == "remote" ]]; then
        source Azure/VMStart.sh "azure"
    else
        PrintHelp
        exit 1
    fi
    ;;

    stop)
    param=""
    if [[ $environment == "local" ]]; then
        param="virtualbox"
    elif [[ $environment == "remote" ]]; then
        param="azure"
    else
        PrintHelp
        exit 1
    fi

    source Common/VMStop.sh $param
    ;;

    create)
    if [[ -z $setupFile ]]; then
        PrintHelp
        exit 1
    elif [[ ! -f $setupFile ]]; then
        printf "Setup file not found.\n"
        exit 1
    fi

    while IFS='' read -r line || [[ -n "$line" ]]; do
        while IFS=',' read -ra currentLine; do
            elementCount=${#currentLine[@]}
            if [[ $environment == "local" ]] && [[ "$elementCount" -gt "2" ]]; then
                source VirtualBox/VMCreate.sh ${currentLine[0]} ${currentLine[1]} ${currentLine[2]}
            elif [[ $environment == "remote" ]] && [[ "$elementCount" -gt "7" ]]; then
                source Azure/VMCreate.sh ${currentLine[0]} ${currentLine[1]} ${currentLine[2]} ${currentLine[3]} ${currentLine[4]} ${currentLine[5]} ${currentLine[6]} ${currentLine[7]}
            fi
        done <<< $line
    done < "$setupFile"
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

    dockerstart)
    if [[ $environment == "local" ]]; then
        source VirtualBox/VMDockerStartup.sh
    elif [[ $environment == "remote" ]]; then
        source Azure/VMDockerStartup.sh
    else
        PrintHelp
        exit 1
    fi
    ;;

    dockerstop)
    param=""
    if [[ $environment == "local" ]]; then
        param="virtualbox"
    elif [[ $environment == "remote" ]]; then
        param="azure"
    else
        PrintHelp
        exit 1
    fi

    source Common/VMDockerStop.sh $param
    ;;

    dockerstats)
    param=""
    if [[ $environment == "local" ]]; then
        param="virtualbox"
    elif [[ $environment == "remote" ]]; then
        param="azure"
    else
        PrintHelp
        exit 1
    fi

    source Common/VMDockerStats.sh $param
    ;;

    dockerlogs)
    param=""
    if [[ $environment == "local" ]]; then
        param="virtualbox"
    elif [[ $environment == "remote" ]]; then
        param="azure"
    else
        PrintHelp
        exit 1
    fi

    source Common/VMDockerLogs.sh $param
    ;;

    *)    # unknown option
    PrintHelp
    ;;
esac
