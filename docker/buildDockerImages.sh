#!/bin/bash

# Get absolute script directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"


cd $DIR'/000_Base'
docker build -t bda/base_image:1.0 .

cd $DIR'/001_Producer'
docker build -t bda/producer:1.0 .

cd $DIR'/002_Kafka/Layer001'
docker build -t bda/kafka:1.0 .

cd $DIR'/002_Kafka/Layer002'
docker build -t bda/kafka:1.1 .

cd $DIR'/003_Storm/Layer001'
docker build -t bda/storm:1.0 .

cd $DIR'/003_Storm/Layer002'
docker build -t bda/storm:1.1 .
