from flask import Flask, render_template
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

    return render_template('index.html')


@app.route('/off')
def off():
    state_store.set("lightson", False)

    return render_template('index.html')


if __name__ == '__main__':
    start()
