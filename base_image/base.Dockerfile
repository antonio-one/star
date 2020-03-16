FROM ubuntu:18.04

# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unset variables as an error when substituting.
# -x Print commands and their arguments as they are executed.
RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y apt-utils \
        build-essential \
        libreadline-gplv2-dev \
        libncursesw5-dev \
        libssl-dev \
        libsqlite3-dev \
        tk-dev \
        libgdbm-dev \
        libc6-dev \
        libbz2-dev \
        libffi-dev \
        zlib1g-dev \
        wget \
        pgp

# install java
RUN apt-get install -y openjdk-8-jdk
RUN update-alternatives --list java
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre

## install python
RUN cd /opt && \
    wget -c https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -O - | tar xvz && \
    cd /opt/Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install
RUN cd /usr/local/bin/ && ln -s python3.7 python
RUN cd /usr/local/bin/ && ln -s pip3.7 pip
