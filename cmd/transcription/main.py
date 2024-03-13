from confluent_kafka import Consumer, KafkaError, KafkaException
from dotenv import load_dotenv
from transcribe import download_video, transcribe, remove_video
import sys
import os
import logging

running = True

def process_message(consumer, msg):
    logging.info("Received url: {}".format(msg.value()))
    url = msg.value().decode('utf-8')
    filename = download_video([url])
    transcription = transcribe(filename)
    remove_video(filename)
    logging.info(transcription)
    consumer.commit(asynchronous=False)

def consume_loop(consumer):
    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.info("%% %s [%d] reached end at offset %d\n" %
                        (msg.topic(), msg.partition(), msg.offset()))
                continue
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            process_message(consumer, msg)

def consume(consumer, topics, producer_function):
    try:
        consumer.subscribe(topics)
        logging.info("Subscribed to topics: {}".format(topics))
        consume_loop(consumer)
    except KafkaException as e:
        logging.error('KafkaException: {}'.format(e))
        return 2
    except Exception as e:
        logging.error('Exception: {}'.format(e))
        return 1
    finally:
        consumer.close()
        shutdown()
    return 0

def shutdown():
    global running
    running = False

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting transcription service")
    load_dotenv("configs/transcription/.env")
    bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")

    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'transcription',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    }

    topics = ['transcription']
    consumer = None
    try:
        logging.info("Attempting to create consumer")
        consumer = Consumer(**conf)
    except Exception as e:
        logging.error('Failed to create consumer: {}'.format(e))
        sys.exit(2)
    result = consume(consumer, topics, lambda key, value: produce(producer, "transcription", key, value))
    sys.exit(result)

if __name__ == "__main__":
    main()
