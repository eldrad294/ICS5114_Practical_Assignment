#!/bin/bash

docker login

docker push nikifrendo/bda_producer:1.0
docker push nikifrendo/bda_kafka:1.1
docker push nikifrendo/bda_storm:1.1
docker push nikifrendo/bda_neo4j:1.0
