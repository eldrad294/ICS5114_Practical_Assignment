FROM ubuntu:16.04

RUN apt-get update                                                                                                      && \
    apt-get install -y software-properties-common python-software-properties                                            && \
    add-apt-repository -y ppa:nilarimogard/webupd8                                                                      && \
    apt-get update                                                                                                      && \
    apt-get upgrade                                                                                                     && \
    apt-get install -y streamlink                                                                                          \
                       python3                                                                                             \
                       python3-pip                                                                                         \
                       ffmpeg                                                                                              \
                       git                                                                                                 \
                       tree                                                                                                \
                       vim                                                                                                 \
                       net-tools                                                                                           \
                       nmap                                                                                                \
                       curl                                                                                             && \
    pip3 install --upgrade pip

RUN pip3 install streamlink                                                                                                \
                 ffmpy                                                                                                     \
                 configparser                                                                                              \
                 pandas                                                                                                    \
                 scipy                                                                                                     \
                 pykafka                                                                                                   \
                 google-cloud-speech                                                                                       \
                 google-cloud-storage

RUN mkdir /root/.ssh                                                                                                    && \
    mkdir /root/src

ADD ./ssh_keys/id_rsa               /root/.ssh/

RUN ssh-keyscan -H github.com >> /root/.ssh/known_hosts                                                                 && \
    cd /root/src                                                                                                        && \
    ssh-agent bash -c 'ssh-add /root/.ssh/id_rsa; git clone git@github.com:eldrad294/ICS5114_Practical_Assignment.git'
