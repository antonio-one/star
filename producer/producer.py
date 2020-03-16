"""
producer.py
"""
from random import randint
from confluent_kafka import Producer
from confluent_kafka.admin import NewTopic
import simplejson as json
from decimal import Decimal
from time import sleep, time as epoch
from uuid import uuid4

# (TODO)Developer find a non-ugly way to import a module from a parent directory
# from ..settings import EnvironmentVariables
# env_vars = EnvironmentVariables(env_file='.env')
# bootstrap_servers = env_vars['BOOTSTRAP_SERVERS']


class Header:
    """
    A header class in case it comes up.
    Not part of the original requirements.
    """
    def __init__(self, unique_id=uuid4(), application_id=None, timestamp=epoch()):
        """
        :param unique_id:
        :param application_id:
        :param timestamp:
        """
        self.unique_id = str(unique_id)
        self.application_id = application_id
        self.timestamp = timestamp

    def get(self):
        header = {"unique_id": self.unique_id, "application_id": self.application_id, "timestamp": self.timestamp}
        return header


class MatchPrice:
    """
    A class that generates synthetic data to populate prices-topic

    Methods
    -------
    rand_match()
        returns a random three-digit number
    rand_price()
        returns a random positive number between 1 and 10
        rounded to the hundredths (2 digits) after the decimal point
    format_message()
        returns
            1. a JSON formatted message like: {"match": 123, "price": 1.38}
            OR
            2. if a header exists a JSON formatted message like:
            {"header": {"application_id": "star_application", "timestamp": 158428978...}, "match": 933, "price": "9.54"}
    """

    def __init__(self, header: Header = None, match=None, price=None):
        """
        Parameters
        ----------
        :param header: a Header() object containing application an timestamp
        :param match: random or manual
        :param price:
        """
        if not match:
            self.match = self.rand_match()
        elif 99 < match < 1000:
            self.match = match
        else:
            raise ValueError(f'Illegal match value: {match}')

        if not price:
            self.price = self.rand_price()
        elif 1 <= price <= 10.0:
            self.price = price
        else:
            raise ValueError(f'Illegal price value: {price}')
        if header:
            self.header = header.get()
        else:
            self.header = None

    @staticmethod
    def rand_match():
        return randint(100, 999)

    @staticmethod
    def rand_price():
        two_places = Decimal(10) ** -2
        this_price = randint(100, 999) / 100
        return Decimal(this_price).quantize(two_places)

    def format_message(self):
        if self.header:
            message = {"header": self.header, "match": self.match, "price": self.price}
        else:
            message = {"match": self.match, "price": self.price}

        return json.dumps(message, use_decimal=True)


class MessageWrapper:
    """
    A simple class to manage the production and acknowledgement of synthetic data

    Methods
    -------
    acked()
        delivery report callback called (from flush()) on successful or failed delivery of the message
    produce_message()
        produce a message
    """
    def __init__(self, topic: NewTopic, message: MatchPrice, producer: Producer):
        """
        :param topic: NewTopic topic object from the kafka-confluent library
        :param message: content
        :param producer: Producer object from the kafka-confluent library
        """
        self.topic = topic
        self.message = message
        self.producer = producer

    def acked(self, error, message):
        if error:
            print(f'failed to deliver message: {error.str()}')
        else:
            print(f'ack received from topic:{message.topic()}, '
                  f'partition:{message.partition()}] '
                  f'and offset: {message.offset()}')

    def produce_message(self):
        # TODO(Developer) May need to add some error catching / retry logic here
        self.producer.produce(self.topic.topic, value=self.message.format_message(), callback=self.acked)
        self.producer.flush(1)


if __name__ == '__main__':
    # TODO(Developer) .env variables instead of hard-coding this
    main_producer = Producer({'bootstrap.servers': 'kafka:9092'})
    # TODO(Developer) Write a separate topic management service
    main_topic = NewTopic('prices-topic', num_partitions=3, replication_factor=1)
    main_header = Header(application_id='star_application')

    while True:
        # TODO(Developer) change to MatchPrice(header=main_header) if you want an imaginary header added
        match_price = MatchPrice()
        print(f'message content: {match_price.format_message()}')
        wrapper = MessageWrapper(main_topic, match_price, main_producer)
        wrapper.produce_message()
        sleep(1)
