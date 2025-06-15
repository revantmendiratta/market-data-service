import os
import json
import time
from confluent_kafka import Consumer, KafkaError
from app.core.database import SessionLocal
from app import crud

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
TOPIC_NAME = 'price-events'
MOVING_AVERAGE_WINDOW = 5

def calculate_moving_average(prices: list) -> float:
    """Calculates the average of a list of numbers."""
    return sum(p.price for p in prices) / len(prices)

def process_message(msg_data: dict):
    """The core logic for processing a new price event."""
    symbol = msg_data.get('symbol')
    new_price = msg_data.get('price')
    
    if not symbol or new_price is None:
        print("Invalid message format, skipping.")
        return

    print(f"Received new price for {symbol}: {new_price}")
    
    # Get a new database session
    db = SessionLocal()
    try:
        # We need N-1 prices from the DB to combine with our 1 new price
        prices_from_db = crud.get_last_n_prices(db, symbol=symbol, n=MOVING_AVERAGE_WINDOW)
        
        # The list from DB is newest-to-oldest, so the new price is the actual latest one.
        # Check if we have enough data points to calculate the moving average.
        if len(prices_from_db) >= MOVING_AVERAGE_WINDOW:
            print(f"Calculating {MOVING_AVERAGE_WINDOW}-point moving average for {symbol}...")
            
            # The list already contains the new price we just saved
            moving_average = calculate_moving_average(prices_from_db)
            
            # Upsert the result into the symbol_averages table
            crud.upsert_moving_average(db, symbol=symbol, moving_average=moving_average)
            
            print(f"Successfully updated moving average for {symbol} to: {moving_average}")
        else:
            print(f"Not enough data yet for {symbol}. Have {len(prices_from_db)}/{MOVING_AVERAGE_WINDOW} points.")
            
    finally:
        db.close()

def main():
    # Kafka Consumer configuration
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'moving_average_consumer_group',
        'auto.offset.reset': 'earliest' # Start reading from the beginning of the topic
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC_NAME])
    
    print("Consumer started. Waiting for messages...")

    try:
        while True:
            # Poll for new messages
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break

            # Message received successfully
            msg_data = json.loads(msg.value().decode('utf-8'))
            process_message(msg_data)
            
    except KeyboardInterrupt:
        print("Consumer shutting down.")
    finally:
        # Cleanly close the consumer
        consumer.close()

if __name__ == '__main__':
    # Give other services a moment to start up before we try to connect
    print("Consumer service starting in 10 seconds...")
    time.sleep(10)
    main()