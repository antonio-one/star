from os import environ
from pyspark.sql import SparkSession

# (TODO)Developer: get the submit_args from .env instead
submit_args = [
    '/opt/spark/jars/spark-streaming-kafka-0-10_2.11-2.4.0.jar',
    '/opt/spark/jars/spark-sql-kafka-0-10_2.11-2.4.0.jar',
    '/opt/spark/jars/kafka-clients-2.4.0.jar'
]

jars = ''
for arg in submit_args:
    jars += f'{arg},'

environ['PYSPARK_SUBMIT_ARGS'] = f' --jars {jars[:-1]} pyspark-shell'

spark = SparkSession \
    .builder \
    .appName('star_consumer') \
    .getOrCreate()

raw_sdf = spark \
    .readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka:9092') \
    .option('subscribe', 'prices-topic')  \
    .option('startingOffsets', 'earliest') \
    .load()

# (TODO)Developer: Automate the schema definitions so both producer.py and consumer.py use it
# (TODO)Developer: Find a way to deserialize the below expression (or use spark.sql later?)
content_sdf = raw_sdf \
    .selectExpr('CAST(value as STRING)')

# raw_sdf \
#     .writeStream \
#     .option("checkpointLocation", "/tmp/checkpoints/raw_sdf/") \
#     .outputMode('append') \
#     .option('truncate', 'false') \
#     .format('console') \
#     .start() \
#     .awaitTermination()

content_sdf \
    .writeStream \
    .option("checkpointLocation", "/tmp/checkpoints/content_sdf/") \
    .outputMode('append') \
    .option('truncate', 'false') \
    .format('console') \
    .queryName('content') \
    .start() \
    .awaitTermination()
