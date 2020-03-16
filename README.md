### Local Version Requirements
```shell script
$ docker-compose --version
docker-compose version 1.25.4, build 8d51620a

$ source venv/bin/activate
(venv) Antonios-MacBook-Air:star antonio$ python --version
Python 3.7.7
```
All docker containers are based on: star/base_image/
which is built with ubuntu:18.04, java 8 and python3.7

Base image repo: [docker hub](https://hub.docker.com/repository/docker/antonioone/juby/general)
To rebuild it in case of error:
```shell script
cd base_image
./build_base_image.sh antonioone juby 0.0.?
```

### Some Testing
Execute the below from the project root before building just in case:
```shell script
python python producer/test_producer.py -v
python python producer/test_consumer.py -v
```

### Logging (a nice to have)
Launch a logging container separately if you want more eyes on what's going on.
It will automatically pick up logs from all locally running containers.
Sign up for a free trial at [loggly](https://www.loggly.com/) and 
get your customer token from https://your_username.loggly.com/tokens
```shell script
export LOGGLY_CUSTOMER_TOKEN=${YOURLOGGLY_CUSTOMER_TOKEN}

#TODO(developer): find out what that @41058 means
docker run --name logspout -d \
    --volume=/var/run/docker.sock:/var/run/docker.sock \
    -e SYSLOG_STRUCTURED_DATA="${LOGGLY_CUSTOMER_TOKEN}@41058" \
    gliderlabs/logspout \
    syslog+tcp://logs-01.loggly.com:514

docker ps -a
```

#### PyCharm specifics
To integrate your IDE with Docker you (may) need busybox
```shell script
docker pull busybox:latest
```
If PyCharm blows up with a "skeleton refresh" error run the below:
```shell script
docker-compose down
docker rm -f $(docker ps -a | grep pycharm_helper | awk '{print $1};')
```
... then invalidate cache and restart

Thread: [Couldn't refresh skeletons](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360000129510-Couldn-t-refresh-skeletons-for-remote-interpreter-Docker)

#### Container hostnames (in order of appearance)

format: project _ service _ 1

- star_zookeeper_1
- star_kafka_1
- star_producer_1
- star_consumer_1

Note: I opted in for a personally home cooked version of zookeeper and kafka dockerfiles instead of using the spotify image. 
The solution is pretty simple(ish) and requires an additional container.

#### Clean start of docker-compose
##### ... depending on level of bravery
```shell script
# docker system prune -a
docker-compose down --remove-orphans --rmi local
docker-compose up --remove-orphans --force-recreate --build 
```

#### Single container rebuild
```shell script
docker-compose up --no-deps --build zookeeper|kafka|producer|consumer
```

#### Remote into a container
```shell script
sudo docker exec -it star_consumer_1 /bin/bash
```

### Kafka topic is auto-created and populated
```shell script
sudo docker exec -it star_kafka_1 /bin/bash
SERVER=kafka:9092
TOPIC=prices-topic
cd /opt/kafka
./bin/kafka-topics.sh --bootstrap-server=${SERVER} --list
./bin/kafka-console-consumer.sh --bootstrap-server=${SERVER} --topic=${TOPIC} --from-beginning
```


#### Other Links
- [More docker syslog notes](https://www.loggly.com/docs/docker-syslog/)
- [logsprout git](https://github.com/gliderlabs/logspout)
- [Application logs](https://antonioone.loggly.com/)
