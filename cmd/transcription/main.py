from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
from dotenv import load_dotenv
from transcribe import download_video, transcribe, remove_video
import sys
import os
import logging

YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
running = True

def process_message(consumer, url, status):
    logging.info("Received url: {}".format(url))
    logging.info("Received status: {}".format(status))

    try:
        filename = download_video([YOUTUBE_BASE_URL + url])
        transcription = transcribe(filename)
        remove_video(filename)
        insert_transcription(url, transcription)
        return url, "done"
    except Exception as e:
        logging.error('Failed to process message: {}'.format(e))
        return url, "failed"
    finally:
        consumer.commit(asynchronous=False)

def consume_loop(consumer, producer_function):
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
            url = msg.key()
            status = msg.value()

            if url is None:
                logging.error("Received message with no key")
            else:
                url = url.decode("utf-8")
            if status is None:
                logging.error("Received message with no value")
            else:
                status = status.decode("utf-8").strip()

            if status and status != "pending":
                logging.info("Skipping message with status: {}".format(status))
                consumer.commit(asynchronous=False)
                continue

            url, status = process_message(consumer, url, status)
            producer_function(url, status)

def consume(consumer, topics, producer_function):
    try:
        consumer.subscribe(topics)
        logging.info("Subscribed to topics: {}".format(topics))
        consume_loop(consumer, producer_function)
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

def produce(producer, topic, key, value):
    producer.produce(topic, key=key, value=value)

def insert_transcription(url, transcription):
    logging.info("Inserting transcription for url: {}".format(url))
    # Insert transcription into database
    # Temporary log transcription to console for testing before database is setup
    logging.info(transcription)

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

    producer = None
    try:
        logging.info("Attempting to create producer")
        producer = Producer({'bootstrap.servers': bootstrap_servers})
    except Exception as e:
        logging.error('Failed to create producer: {}'.format(e))
        sys.exit(2)

    result = consume(consumer, topics, lambda key, value: produce(producer, "transcription", key, value))
    producer.flush()
    sys.exit(result)

if __name__ == "__main__":
    main()
