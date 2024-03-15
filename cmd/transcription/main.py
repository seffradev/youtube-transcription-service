from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
from dotenv import load_dotenv
from transcribe import download_video, transcribe, remove_video
from sqlalchemy import create_engine, insert, Column, String, Integer, Text, DateTime, Enum
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime
import sys
import os
import logging

Base = declarative_base()

YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
running = True

class Transcription(Base):
    __tablename__ = 'transcription'
    id = Column(String(11), primary_key=True)
    status = Column(Enum('pending', 'in_progress', 'completed', 'failed'), nullable=False)
    text = Column(Text)
    requested_at = Column(DateTime, nullable=False, default=datetime.now())
    completed_at = Column(DateTime)
    cost = Column(Integer)

    def __repr__(self):
        return "<Transcription(id='{}', status='{}', text='{}', requested_at='{}', completed_at='{}', cost='{}')>".format(self.id, self.status, self.text, self.requested_at, self.completed_at, self.cost)

def process_message(database, consumer, url, status):
    logging.info("Received url: {}".format(url))
    logging.info("Received status: {}".format(status))

    try:
        filename = download_video([YOUTUBE_BASE_URL + url])
        transcription = transcribe(filename)
        remove_video(filename)
        insert_transcription(database, url, transcription)
        return url, "done"
    except Exception as e:
        logging.error('Failed to process message: {}'.format(e))
        return url, "failed"
    finally:
        consumer.commit(asynchronous=False)

def consume_loop(database, consumer, producer_function):
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

            url, status = process_message(database, consumer, url, status)
            producer_function(url, status)

def consume(database, consumer, topics, producer_function):
    try:
        consumer.subscribe(topics)
        logging.info("Subscribed to topics: {}".format(topics))
        consume_loop(database, consumer, producer_function)
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

def insert_transcription(database, url, transcription):
    logging.info("Inserting transcription for url: {}".format(url))
    transcription_to_update = database.query(Transcription).filter(Transcription.id == url).one_or_none()
    if transcription_to_update:
        transcription_to_update.status = "completed"
        transcription_to_update.text = transcription
        transcription_to_update.completed_at = datetime.now()
        database.commit()
        logging.info("Updated transcription for url: {}".format(url))
    else:
        logging.error("Transcription not found for url: {}".format(url))

def shutdown():
    global running
    running = False

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting transcription service")
    load_dotenv("configs/transcription/.env")
    bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
    database_url = os.getenv("DATABASE_URL")

    if not bootstrap_servers:
        logging.error("BOOTSTRAP_SERVERS not set")
        sys.exit(1)

    if not database_url:
        logging.error("DATABASE_URL not set")
        sys.exit(1)

    database = create_engine("mysql+pymysql://" + database_url)

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

    with Session(database) as session:
        result = consume(session, consumer, topics, lambda key, value: produce(producer, "transcription", key, value))

    producer.flush()
    sys.exit(result)

if __name__ == "__main__":
    main()
