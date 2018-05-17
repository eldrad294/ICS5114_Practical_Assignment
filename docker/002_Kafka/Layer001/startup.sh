#!/bin/bash

cp -f /root/kafka.server.properties.template /root/kafka.server.properties

if [[ -z $kafka_host_ip ]]; then
    printf "Environment variable 'kafka_host_ip' not set. Aborting.\n"
    exit 1
fi

listenerConfig="advertised.listeners=PLAINTEXT://$kafka_host_ip:9092"
echo $listenerConfig >> /root/kafka.server.properties
mv -f /root/kafka.server.properties /opt/kafka_2.11-1.1.0/config/

# Start zookeeper server
/bin/bash /opt/zookeeper-3.4.12/bin/zkServer.sh start

# Start kafka server
# Note: Triggering the kafka server scripts holds control of the terminal session. Therefore, the kafka script
#       is forked and called as a separate OS process. Control is required as we need to create kafka topics
#       after starting the server.
mkdir -p /tmp/bda_kafka_logs
/bin/bash /opt/kafka_2.11-1.1.0/bin/kafka-server-start.sh /opt/kafka_2.11-1.1.0/config/kafka.server.properties > /tmp/bda_kafka_logs/kafka.logs &

# Ensure kafka server is up before progressing further
while true
do
  sleep 10

  kafkaProc="$(jps)"
  if echo "$kafkaProc" | grep -q "QuorumPeerMain"; then
    break
  fi
done

# Kafka server up, create kafka topic/s
/opt/kafka_2.11-1.1.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic video
/opt/kafka_2.11-1.1.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic text

# Read kafka server output and keep OS process in memory
tail -f /tmp/bda_kafka_logs/kafka.logs
