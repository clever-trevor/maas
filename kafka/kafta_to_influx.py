#!/usr/bin/python3

# Script to push metrics from Kafka to InfluxDB
from influxdb import InfluxDBClient,SeriesHelper

client = InfluxDBClient(host='localhost', port=8086, database='kafka')
client.create_database('kafka')

from kafka import KafkaConsumer
from kafka.structs import OffsetAndMetadata, TopicPartition

consumer = KafkaConsumer(bootstrap_servers=['localhost:9101'])
consumer.subscribe('telegraf')

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

for msg in consumer:
  data = msg.value.decode("utf-8")
#  print(data)

  client.write_points(data, protocol="line")
#  consumer.commit()

