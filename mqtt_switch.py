import paho.mqtt.client as mqtt
from threading import Thread
import time


class MQTTCommands:
    def __init__(self):
        pass

    def make_action(self, msg='Guy', def1='GPIO_ON'):
        global GPIO1_ON
        if msg.payload.decode() == 'Guy':
            print("action1")
            GPIO1_ON()
        elif msg.payload.decode() == 'Dvir':
            print("action2")
        else:
            print("Donno")


class MQTTClient(Thread, MQTTCommands):
    def __init__(self, sid=None, host="iot.eclipse.org", username=None, password=None, topic=None, topic_qos=None):
        Thread.__init__(self)
        MQTTCommands.__init__(self)
        self.sid = sid
        self.host = host
        self.username = username
        self.password = password
        self.topic = topic
        self.topic_qos = topic_qos
        self.client = None

    def on_connect(self, client, obj, flags, rc):
        print(">> Connecting to MQTT server %s: %d" % (self.host, rc))
        self.client.subscribe(self.topic, qos=self.topic_qos)

    def on_message(self, client, obj, msg):
        print(">> received: topic:%s msg:%s " % (msg.topic, msg.payload.decode()))
        if msg.payload.decode() in self.ext_commands:
            print(self.ext_commands[msg.payload.decode()])
        self.make_action(msg)

    def pub(self, payload):
        self.client.publish(self.topic, payload, self.topic_qos)
        print(">> published: topic:%s msg:%s " % (self.topic, payload))

    def run(self):
        self.client = mqtt.Client(str(self.sid))
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        if self.username is not None and self.password is not None:
            self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.host, 1883, 60)
        self.client.loop_forever()

    def commands(self, com_dic):
        self.ext_commands = com_dic
        print(com_dic)


def GPIO1_ON():
    print("GPIO_ON")


if __name__ == "__main__":
    a = MQTTClient(topic='HomePi/dvir/test1', topic_qos=0, host='192.168.2.113')
    # a.commands({'On': 'action1', 'Off': 'action2'})
    a.start()
    a.pub("Guy")
    # b = MQTTCommands()
    # getattr(b, 'make_action')
