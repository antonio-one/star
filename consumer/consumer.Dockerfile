FROM antonioone/juby:latest

ENV JARS_DIR=/opt/spark/jars \
    MAVEN=https://repo1.maven.org/maven2/org/apache

# Download apache spark
#TODO(Developer): Verify download.
RUN cd /opt && \
    wget https://mirrors.ukfast.co.uk/sites/ftp.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz -O - | tar xvz
RUN cd /opt && \
    ln -s spark-2.4.5-bin-hadoop2.7 spark

#TODO(Developer): get the artifacts from .env instead - it's also used by consumer.py to set the PYSPARK_SUBMIT_ARGS
# Download jars
RUN for artifact in \
        ${MAVEN}/spark/spark-streaming-kafka-0-10_2.11/2.4.0/spark-streaming-kafka-0-10_2.11-2.4.0.jar \
        ${MAVEN}/spark/spark-sql-kafka-0-10_2.11/2.4.0/spark-sql-kafka-0-10_2.11-2.4.0.jar \
        ${MAVEN}/kafka/kafka-clients/2.4.0/kafka-clients-2.4.0.jar \
    ; do \
        echo ${artifact}; \
        wget -c ${artifact} -O ${JARS_DIR}/$(basename ${artifact}); \
    done;

#        ${MAVEN}/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.0/spark-streaming-kafka-0-8-assembly_2.11-2.4.0.jar \


WORKDIR /consumer
COPY ./requirements.txt /consumer/requirements.txt
RUN pip install -r /consumer/requirements.txt
COPY consumer.py /consumer/

CMD ["python", "-u", "consumer.py"]
#CMD ["tail", "-f", "/dev/null"]
