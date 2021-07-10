from kafka import KafkaConsumer
from json import loads
from time import sleep

TOPIC_NAME = 'topic_hello'
CHECK_DELAY = 10  # checking for messages every 20 seconds
# kafka doesn't start immediately in a container so we need to wait before connecting
STARTUP_DELAY = 11


def connect():
    sleep(STARTUP_DELAY)
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=None,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        return consumer
    except Exception as e:
        print(f'Consumer couldn\'t connect: {e}', flush=True)
        return None


def main():
    consumer = connect()
    if consumer is None:
        return

    print('Kafka consumer: listening to messages', flush=True)

    for event in consumer:
        print(event.value, flush=True)
        sleep(CHECK_DELAY)


if __name__ == '__main__':
    main()
