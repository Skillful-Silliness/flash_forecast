from flask import Flask, jsonify, request, send_from_directory
import state_store
import sys

BRIGHTNESS_INCREMENT = 0.05

app = Flask(__name__, static_url_path='/', static_folder='public')

def start():
    app.run(host='0.0.0.0', port=80)


def json_response_with_cors(body):
    response = jsonify(body)

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/')
def index():
    return send_from_directory("./public", 'index.html')


@app.route('/api/on')
def on():
    state_store.set("lights_on", True)

    return json_response_with_cors({"lightsOn": True})


@app.route('/api/off')
def off():
    state_store.set("lights_on", False)

    return json_response_with_cors({"lightsOn": False})


@app.route('/api/status')
def status():
    state_store.get_all()
    try:
        all_data = state_store.get_all()

        status_for_json = {
            "brightness": all_data["brightness"],
            "lightsOn": all_data["lights_on"],
            "currentWeather": all_data["data"]["current_weather"]
        }

        return json_response_with_cors(status_for_json)
    except:
        return json_response_with_cors({"error": sys.exc_info()[0]})


@app.route('/api/debug')
def debug():
    return json_response_with_cors(state_store.get_all())

@app.route('/api/brighter')
def brighter():
    val = state_store.get("brightness")

    val = min(val + BRIGHTNESS_INCREMENT, 1)

    state_store.set("brightness", val)

    return json_response_with_cors({"brightness": val})


@app.route('/api/brightness')
def brightness():
    val = float(request.args.get('v'))
    val = max(0, min(val, 1))

    state_store.set("brightness", val)

    return json_response_with_cors({"brightness": val * 100})

@app.route('/api/darker')
def darker():
    val = state_store.get("brightness")

    val = max(val - BRIGHTNESS_INCREMENT, 0)

    state_store.set("brightness", val)

    return json_response_with_cors({"brightness": val})


if __name__ == '__main__':
    start()
