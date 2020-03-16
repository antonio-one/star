FROM antonioone/juby:latest

WORKDIR /producer
COPY ./requirements.txt /producer/requirements.txt
RUN pip install -r /producer/requirements.txt
COPY producer.py /producer/
CMD ["python", "-u", "producer.py"]