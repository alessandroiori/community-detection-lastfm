#!/usr/bin/env python
from kafka import KafkaConsumer

class Consumer():
    def __init__(self):
        consumer = KafkaConsumer('messages',
                                 bootstrap_servers=['192.168.99.100:9092'],
                                 auto_offset_reset='latest',
                                 enable_auto_commit=True,
                                 auto_commit_interval_ms=500,
                                 consumer_timeout_ms=3000)

        for message in consumer:
            print ("Consumed Msg -> '%s' on Topic -> '%s' with Offset -> %d" %
                    (message.value.decode('utf-8'), message.topic, message.offset))
        consumer.close()
