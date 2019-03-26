from flask import Flask, render_template
from src.model.MQTTClient import MQTTClient

app = Flask(__name__, template_folder='./views')


def start_application():
    app.run()


def start_mqtt_client():
    broker, port = 'localhost', 1883
    my_client = MQTTClient()
    my_client.start(broker, port)


@app.route('/')
def hello_world():
    return render_template('graph.html')


if __name__ == '__main__':
    start_mqtt_client()
    start_application()
