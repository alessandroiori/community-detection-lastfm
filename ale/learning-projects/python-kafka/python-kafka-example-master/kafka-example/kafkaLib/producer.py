#!/usr/bin/env python
from kafka import KafkaProducer

class Producer():
    def __init__(self):
        producer = KafkaProducer(bootstrap_servers=['192.168.99.100:9092'], retries=5)
        producer.send('messages', b'super-duper-message')
        print("Published msg -> 'super-duper-message' on Topic -> 'messages'")
        # block until all async messages are sent
        producer.flush()
        # tidy up the producer connection
        producer.close()
