#!/usr/bin/env python
import threading, logging, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer

topic = 'test:1:1'
kafka_server = 'localhost:9092' #'192.168.99.100:9092'


class Producer(threading.Thread):
    daemon = True

    def run(self):
        print("producer connetting")
        producer = KafkaProducer(bootstrap_servers=kafka_server)

        print("producer sending")
        while True:
            print("send")
            producer.send(topic, b"test")
            #producer.send(topic, b"\xc2Hello, world!")
            time.sleep(1)


class Consumer(multiprocessing.Process):
    daemon = True

    def run(self):
        print("consumer connetting")
        consumer = KafkaConsumer(bootstrap_servers=kafka_server,
                                 auto_offset_reset='earliest')
        print("consumer subscribe")
        consumer.subscribe([topic])

        print("consumer reading")
        for message in consumer:
            print("read")
            print(message)


def main():
    tasks = [
        Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
