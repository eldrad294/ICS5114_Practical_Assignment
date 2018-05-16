#!/bin/bash

# echo $1
# echo $2

echo "Param_01 --> $1"
echo "Param_02 --> $2"



existingVMs=$(docker-machine ls --filter name=$1* --filter driver=virtualbox --format={{.Name}})

if [ -n "$existingVMs" ] && [ $1 -ne "neo4j" ]; then
  docker-machine rm -y $existingVMs
fi
