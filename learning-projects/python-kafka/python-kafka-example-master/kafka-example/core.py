from kafkaLib import producer as KP
from kafkaLib import consumer as KC

def run():
    # Start the Kafka producer
    KP.Producer()
    # Start the Kafka Consumer
    KC.Consumer()
