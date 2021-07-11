from kafka import KafkaConsumer
from influxdb import InfluxDBClient
from json import loads
from time import sleep

KAFKA_HOST = 'kafka'
KAFKA_PORT = 9092
INFLUX_HOST = 'influxdb'
INFLUX_PORT = 8086
INFLUX_DB_NAME = 'detector_data'

TOPIC_NAME = 'topic_detector'
CHECK_DELAY = 1  # checking for messages every second

def connect_to_kafka():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='detector-group',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        return consumer
    except Exception as e:
        print(f'Consumer couldn\'t connect: {e}', flush=True)
        return None


def connect_to_influx():
    try:
        client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT, username='grafana', password='password')
        client.create_database('detector_data')
        client.switch_database('detector_data')
        return client
    except Exception as e:
        print(f'Couldn\'t connect to InfluxDB: {e}', flush=True)
        return None


def get_json_message(message):
    message_json = loads(message)
    return [
        {
            'measurement': 'coords',
            'fields': coords
        }
        for coords in message_json['coords']
    ]


def main():
    consumer = connect_to_kafka()
    influx_client = connect_to_influx()
    if consumer is None or influx_client is None:
        return

    print('Kafka consumer: listening to messages', flush=True)

    for event in consumer:
        message = event.value
        print(message, flush=True)
        influx_client.write_points(get_json_message(message))
        consumer.commit()
        sleep(CHECK_DELAY)


if __name__ == '__main__':
    sleep(10)
    main()
