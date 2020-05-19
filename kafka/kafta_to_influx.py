#!/usr/bin/python3

# Script to push metrics from Kafka to InfluxDB
from influxdb import InfluxDBClient,SeriesHelper

client = InfluxDBClient(host='localhost', port=8086, database='telegraf')
#client.create_database('telegraf')

from kafka import KafkaConsumer
from kafka.structs import OffsetAndMetadata, TopicPartition

consumer = KafkaConsumer(bootstrap_servers=['localhost:9101'])
consumer.subscribe('telegraf')

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *
counter = 0
for msg in consumer:
  data = msg.value.decode("utf-8")
  #counter = counter + 1
  #if counter % 100 == 0 :
  #  print(counter)

  client.write_points(data, protocol="line")
#  consumer.commit()

