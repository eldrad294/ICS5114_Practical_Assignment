FROM bda/base_image:1.0

RUN apt-get install -y default-jdk

ADD ./kafka_2.11-1.1.0.tgz    /opt
ADD ./zookeeper-3.4.12.tar.gz /opt
ADD ./startup.sh              /root