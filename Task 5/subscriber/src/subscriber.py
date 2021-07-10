import paho.mqtt.client as mqtt

# MQTT constants
BROKER = 'mosquitto'
PORT = 1883
TOPIC_NAME = 'opencv/coords'

def on_connect(client, userdata, flags, rc):
    print(f'Subscriber connected with status code {str(rc)}', flush=True)
    client.subscribe(TOPIC_NAME)


def on_message(client, userdata, msg):
    print(msg.payload.decode(), flush=True)


def main():
    client = mqtt.Client('OpenCV detector subscriber')
    if client.connect(BROKER, PORT):
        print("Error while connecting to MQTT, exiting...")
        return
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
    

if __name__ == '__main__':
    main()
