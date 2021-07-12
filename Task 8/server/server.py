from flask import Flask
from flask_caching import Cache
import paho.mqtt.client as mqtt

BROKER = 'mosquitto'
PORT = 1883

config = {
    'DEBUG': True,
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
cache.set('current_mode', 'play')

client = mqtt.Client('Server publisher')

# curl http://localhost:5000/mode
@app.route('/mode', methods=['GET'])
def get_mode():
    return cache.get('current_mode')


# curl -X POST http://localhost:5000/play
@app.route('/play', methods=['POST'])
def set_play_mode():
    if cache.get('current_mode') == 'pause':
        client.connect(BROKER, PORT)
        cache.set('current_mode', 'play')
        client.publish(topic='flask/change_mode', payload='play', retain=True)
        client.disconnect()
        return 'Unpausing the script!'

    return 'Already in play mode, skipping'

# curl -X POST http://localhost:5000/pause
@app.route('/pause', methods=['POST'])
def set_pause_mode():
    if cache.get('current_mode') == 'play':
        client.connect(BROKER, PORT)
        cache.set('current_mode', 'pause')
        client.publish(topic='flask/change_mode', payload='pause', retain=True)
        client.disconnect()
        return 'Pausing the script!'

    return 'Already in pause mode, skipping'   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
