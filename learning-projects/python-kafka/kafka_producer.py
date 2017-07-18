"""""
from kafka import KafkaProducer

def start_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    for i in range(100):
        producer.send('topic_test', b'message ' + str(i))

print("Start producer")
start_producer()
"""""

from kafka import SimpleProducer, SimpleClient

# To send messages asynchronously
client = SimpleClient('localhost:9092')
producer = SimpleProducer(client, async=True)
producer.send_messages('my-topic', b'async message')

# To send messages in batch. You can use any of the available
# producers for doing this. The following producer will collect
# messages in batch and send them to Kafka after 20 messages are
# collected or every 60 seconds
# Notes:
# * If the producer dies before the messages are sent, there will be losses
# * Call producer.stop() to send the messages and cleanup
producer = SimpleProducer(client,
                          async=True,
                          batch_send_every_n=20,
                          batch_send_every_t=60)

