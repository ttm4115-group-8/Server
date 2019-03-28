from flask import Flask, render_template, redirect, url_for
from flask_mqtt import Mqtt

app = Flask(__name__, template_folder='./views')
app.config['MQTT_BROKER_URL'] = '129.241.208.68'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0

mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('#')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    update_template()


def update_template():
    return redirect(url_for('.index', val="HEY"))


@app.route('/')
def index():
    return render_template('graph.html')
