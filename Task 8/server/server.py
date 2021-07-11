from flask import Flask, session
from flask_caching import Cache

config = {
    'DEBUG': True,
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
cache.set('current_mode', 'play')

# curl http://localhost:5000/mode
@app.route('/mode', methods=['GET'])
def get_mode():
    return cache.get('current_mode')


# curl -X POST http://localhost:5000/play
@app.route('/play', methods=['POST'])
def set_play_mode():
    if cache.get('current_mode') == 'pause':
        cache.set('current_mode', 'play')
        return 'Unpausing the script!'

    return 'Already in play mode, skipping'

# curl -X POST http://localhost:5000/pause
@app.route('/pause', methods=['POST'])
def set_pause_mode():
    if cache.get('current_mode') == 'play':
        cache.set('current_mode', 'pause')
        return 'Pausing the script!'

    return 'Already in pause mode, skipping'   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
