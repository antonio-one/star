FROM antonioone/juby:latest

ENV KAFKA_HOME=/opt/kafka \
    PATH="${KAFKA_HOME}/bin:${PATH}" \
    ADVERTISED_HOST=kafka \
    ADVERTISED_PORT=9092 \
    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre


# download kafka
#TODO(developer): Verify download. See example in zookeeper.Dockerfile
RUN cd /opt && \
    wget -c http://mirror.ox.ac.uk/sites/rsync.apache.org/kafka/2.4.0/kafka_2.12-2.4.0.tgz -O - | tar xvz
RUN cd /opt && \
    ln -sf kafka_2.12-2.4.0 kafka

# Points kafka to the internal network address, localhost doesn't work.
#RUN sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect=zookeeper:2181/g' ${KAFKA_HOME}/config/server.properties
COPY server.properties ${KAFKA_HOME}/config/
CMD ${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/server.properties
