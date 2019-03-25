import paho.mqtt.client as mqtt
from threading import Thread


class MQTT_Client:

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print('on_connect(): {}'.format(mqtt.connack_string(rc)))

    def on_message(self, client, userdata, msg):
        print('on_message(): {}'.format(msg.topic))

    def start(self, broker, port):
        print('Connecting to {}:{}'.format(broker, port))

        self.client.connect(broker, port)

        # TODO: Possibly replace '#' with correct channgel
        self.client.subscribe("#")

        try:
            thread = Thread(target=self.client.loop_forever())
            thread.start()
        except KeyboardInterrupt:
            print('Interrupted')
            self.client.disconnect()
