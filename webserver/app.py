from flask import Flask, jsonify, render_template
import state_store
import sys

BRIGHTNESS_INCREMENT = 0.05

app = Flask(__name__)


def start():
    app.run(host='0.0.0.0', port=80)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/on')
def on():
    state_store.set("lightson", True)

    return jsonify({"lightson": True})


@app.route('/off')
def off():
    state_store.set("lightson", False)

    return jsonify({"lightson": False})


@app.route('/status')
def status():
    try:
        return jsonify(state_store.get_all())
    except:
        return jsonify({"error": sys.exc_info()[0]})


@app.route('/brighter')
def brighter():
    val = state_store.get("brightness")

    val = min(val + BRIGHTNESS_INCREMENT, 1)

    state_store.set("brightness", val)

    return jsonify({"brightness": val})


@app.route('/darker')
def darker():
    val = state_store.get("brightness")

    val = max(val - BRIGHTNESS_INCREMENT, 0)

    state_store.set("brightness", val)

    return jsonify({"brightness": val})


if __name__ == '__main__':
    start()
