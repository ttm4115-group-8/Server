from flask import Flask
from MQTT_Client import MQTT_Client
from threading import Thread

app = Flask(__name__)


def start_application():
    app.run()


def start_mqtt_client():
    broker, port = '129.241.208.68', 1883
    my_client = MQTT_Client()
    my_client.start(broker, port)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    thread1 = Thread(target=start_application)
    thread2 = Thread(target=start_mqtt_client)

    thread1.start()
    thread2.start()
