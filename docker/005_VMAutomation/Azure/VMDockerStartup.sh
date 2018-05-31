#!/bin/bash

RunKafkaContainer()
{
    imageName=$(docker-machine ssh $2 "sudo docker images --filter=reference='nikifrendo/*kafka:*' --format={{.Repository}}:{{.Tag}}")
    docker-machine ssh $2 "sudo docker run --rm -d --memory=2g --publish 2181:2181 --publish 9092:9092 -e kafka_host_ip=$1 --name kafka $imageName" >/dev/null 2>&1

    printf "ZooKeeper.."
    while true; do
        sleep 5
        zooKeeperPort=$(docker-machine ssh $2 "sudo nmap -p 2181 127.0.0.1" | grep open)

        if [[ ! -z $zooKeeperPort ]]; then
            printf "running.\n"
            break
        else
            printf "."
        fi
    done

    printf "Kafka.."
    while true; do
        sleep 5
        kafkaPort=$(docker-machine ssh $2 "sudo nmap -p 9092 127.0.0.1" | grep open)

        if [[ ! -z $kafkaPort ]]; then
            printf "running.\n"
            break
        else
            printf "."
        fi
    done
}

RunNeo4J()
{
    imageName=$(docker-machine ssh $2 "sudo docker images --filter=reference='nikifrendo/*neo4j:*' --format={{.Repository}}:{{.Tag}}")
    docker-machine ssh $2 "sudo docker run --rm -d --memory=2g --publish=7474:7474 --publish=7687:7687 --volume=/mnt/sda1/neo4j/data:/data --name neo4j $imageName" >/dev/null 2>&1

    printf "Neo4j WebServer.."
    while true; do
        sleep 5
        webServerPort=$(docker-machine ssh $2 "sudo nmap -p 7474 127.0.0.1" | grep open)

        if [[ ! -z $webServerPort ]]; then
            printf "running.\n"
            break
        else
            printf "."
        fi
    done

    printf "Bolt service.."
    while true; do
        sleep 5
        boltPort=$(docker-machine ssh $2 "sudo nmap -p 7687 127.0.0.1" | grep open)

        if [[ ! -z $boltPort ]]; then
            printf "running.\n"
            break
        else
            printf "."
        fi
    done
}

RunStorm()
{
    imageName=$(docker-machine ssh $2 "sudo docker images --filter=reference='nikifrendo/*storm:*' --format={{.Repository}}:{{.Tag}}")
    docker-machine ssh $2 "sudo docker run --rm -d --memory=2g -e kafka_connection_strings=$3 -e zookeeper_connection=$4 -e neo4j_connection_string=$5 --name storm $imageName" >/dev/null 2>&1

    printf "Storm service.."
    while true; do
        stormProcCount=$(docker-machine ssh $2 "ps aux | grep streamparse_run -c")

        # Conservatively sleeping before checking if all processes are up.
        sleep 30

        if [[ $stormProcCount -gt "5" ]]; then
            printf "running.\n"
            break
        else
            printf "."
        fi
    done
}

RunProducer()
{
    while true; do
        printf "* Enter video source offset ($2): "
        read userSelection

        # Check if userSelection is an integer, otherwise break out.
        if [[ $userSelection =~ ^-?[0-9]+$ ]]; then
            imageName=$(docker-machine ssh $2 "sudo docker images --filter=reference='nikifrendo/*producer:*' --format={{.Repository}}:{{.Tag}}")
            docker-machine ssh $2 "sudo docker run --rm -d --memory=2g -e kafka_connection_strings=$1 -e stream_offset=$userSelection --name producer$userSelection $imageName" >/dev/null 2>&1
        else
            printf "$2 - Complete.\n\n"
            break
        fi
    done
}


# Validation --> at least one of each container should be running
arrayVMs=($(docker-machine ls -t 60 --filter driver=azure --filter state=running --format={{.Name}}))

result=0

ipAddrKafka=""
ipAddrStorm=""
ipAddrNeo4j=""
ipAddrProducers=""

vmNameKafka=""
vmNameStorm=""
vmNameNeo4j=""
vmNameProducers=""

idxProducer=0

for (( i=0; i<${#arrayVMs[@]}; i++ )); do
    if [[ ${arrayVMs[$i]} = *"kafka"* ]]; then
        result=$(($result|1))
        vmNameKafka=$(echo ${arrayVMs[$i]} | sed 's/__.*//')
        ipAddrKafka=$(docker-machine ssh $vmNameKafka "ifconfig eth0 | grep 'inet addr' | cut -d: -f2" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
    elif [[ ${arrayVMs[$i]} = *"storm"* ]]; then
        result=$(($result|2))
        vmNameStorm=$(echo ${arrayVMs[$i]} | sed 's/__.*//')
        ipAddrStorm=$(docker-machine ssh $vmNameStorm "ifconfig eth0 | grep 'inet addr' | cut -d: -f2" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
    elif [[ ${arrayVMs[$i]} = *"producer"* ]]; then
        result=$(($result|4))
        vmNameProducers[$idxProducer]=$(echo ${arrayVMs[$i]} | sed 's/__.*//')
        ipAddrProducers[$idxProducer]=$(docker-machine ssh ${vmNameProducers[$idxProducer]} "ifconfig eth0 | grep 'inet addr' | cut -d: -f2" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
        idxProducer=$((idxProducer+1))
    elif [[ ${arrayVMs[$i]} = *"neo4j"* ]]; then
        result=$(($result|8))
        vmNameNeo4j=$(echo ${arrayVMs[$i]} | sed 's/__.*//')
        ipAddrNeo4j=$(docker-machine ssh $vmNameNeo4j "ifconfig eth0 | grep 'inet addr' | cut -d: -f2" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
    fi
done

if [[ $result != 15 ]]; then
    printf "Not all VMs are running. Error code: $result.\n"
    exit 1
fi


kafkaConnectionString=$ipAddrKafka":9092"
zooKeeperConnectionString=$ipAddrKafka":2181"
neo4jConnectionString="bolt://$ipAddrNeo4j:7687"


if [[ ${#vmNameProducers[@]} != ${#ipAddrProducers[@]} ]]; then
    printf "Producer configuration inconsistent. Aborting docker container startup.\n"
else
    RunKafkaContainer $ipAddrKafka $vmNameKafka
    RunNeo4J $ipAddrNeo4j $vmNameNeo4j
    RunStorm $ipAddrStorm $vmNameStorm $kafkaConnectionString $zooKeeperConnectionString $neo4jConnectionString

    for (( i=0; i<${#vmNameProducers[@]}; i++ )); do
        printf "${vmNameProducers[$i]} - Container startup\n"
        RunProducer $kafkaConnectionString ${vmNameProducers[$i]}
    done


    printf "Docker containers started.\n"
fi
