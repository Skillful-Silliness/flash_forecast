from flask import Flask, jsonify, render_template
import state_store

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


@app.route('/brightness')
def brightness():
    return jsonify({"brightness": state_store.get("brightness")})


@app.route('/brighter')
def brighter():
    val = state_store.get("brightness")

    val = min(val + 0.1, 1)

    state_store.set("brightness", val)

    return jsonify({"brightness": val})


@app.route('/darker')
def darker():
    val = state_store.get("brightness")

    val = max(val - 0.1, 0)

    state_store.set("brightness", val)

    return jsonify({"brightness": val})


if __name__ == '__main__':
    start()
