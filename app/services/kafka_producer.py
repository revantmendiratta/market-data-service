import os
import json
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')

# Create a Kafka producer instance.
# The configuration settings are for connecting to the Kafka broker.
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_price_event(price_data: dict):
    """
    Produces a price event message to the 'price-events' Kafka topic.
    """
    # The topic we want to send messages to
    topic = 'price-events'
    
    # Trigger delivery report callbacks
    producer.poll(0)
    
    # Asynchronously produce a message. The message is JSON encoded.
    producer.produce(
        topic, 
        json.dumps(price_data).encode('utf-8'), 
        callback=delivery_report
    )
    
    # Wait for any outstanding messages to be delivered and delivery reports to be received.
    producer.flush()