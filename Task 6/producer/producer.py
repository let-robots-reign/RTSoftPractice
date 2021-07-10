from time import sleep
from json import dumps
from kafka import KafkaProducer

TOPIC_NAME = 'topic_hello'
SEND_DELAY = 10  # sending a message every 10 seconds
# kafka doesn't start immediately in a container so we need to wait before connecting
STARTUP_DELAY = 10


def connect():
    sleep(STARTUP_DELAY)
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
        return producer
    except Exception as e:
        print(f'Producer couldn\'t connect: {e}', flush=True)
        return None


def main():
    producer = connect()
    if producer is None:
        return

    print('Kafka producer: sending messages', flush=True)

    while True:
        msg = 'Hello, let-robots-reign!'
        producer.send(TOPIC_NAME, value=msg)
        sleep(SEND_DELAY)


if __name__ == '__main__':
    main()
