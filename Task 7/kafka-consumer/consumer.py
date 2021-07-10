from kafka import KafkaConsumer
from json import loads
from time import sleep

TOPIC_NAME = 'topic_detector'
CHECK_DELAY = 1  # checking for messages every second

def connect():
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
    sleep(10)
    main()
