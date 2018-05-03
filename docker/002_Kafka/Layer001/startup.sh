#!/bin/bash

/bin/bash /opt/zookeeper-3.4.12/bin/zkServer.sh start
/bin/bash /opt/kafka_2.11-1.1.0/bin/kafka-server-start.sh /opt/kafka_2.11-1.1.0/config/server.properties