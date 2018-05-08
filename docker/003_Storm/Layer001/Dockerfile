FROM bda/base_image:1.0

ENV LEIN_ROOT true
ENV PATH="$PATH:/root/apache-storm-1.2.1/bin"

ADD ./lein                       /usr/bin
ADD ./apache-storm-1.2.1.tar.gz  /root

RUN apt-get install -y default-jdk
RUN /bin/bash /usr/bin/lein
