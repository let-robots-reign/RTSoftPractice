import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from json import dumps
from time import sleep

# MQTT constants
BROKER = 'mosquitto'
PORT = 1883
MQTT_TOPIC_NAME = 'opencv/coords'
KAFKA_TOPIC_NAME = 'topic_detector'


def on_connect(client, userdata, flags, rc):
    print(f'Subscriber connected with status code {str(rc)}', flush=True)
    client.subscribe(MQTT_TOPIC_NAME)


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    producer = userdata['kafka_producer']
    producer.send(KAFKA_TOPIC_NAME, value=message)


def main():
    # it's both a mqtt subscriber and a kafka producer
    # connecting to kafka producer
    producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    client = mqtt.Client('OpenCV detector subscriber', userdata={'kafka_producer': producer})
    if client.connect(BROKER, PORT):
        print("Error while connecting to MQTT, exiting...")
        return
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
    

if __name__ == '__main__':
    sleep(10)
    main()
