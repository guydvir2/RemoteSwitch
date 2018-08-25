import paho.mqtt.client as mqtt
from threading import Thread
import datetime
import os


class MQTTlogger(Thread):
    def __init__(self, sid=None, host="192.168.2.113", username=None,
                 password=None, topics=None, topic_qos=None, filename='/Users/guy/MQTT.log'):
        Thread.__init__(self)
        self.sid = sid
        self.host = host
        self.filename = filename
        self.username = username
        self.password = password
        self.topics = topics
        self.topic_qos = topic_qos
        self.output2screen = 1
        self.client, self.arrived_msg = None, None

        self.check_logfile_valid()
        self.log_header()

    def log_header(self):
        tmp = ''
        topics_text = ["%d)Topic: %s" % (i, topic) for i, topic in enumerate(self.topics)]
        for text in topics_text:
            tmp = tmp + '\n' + text
        self.append_log("\nMQTT logger for Topics: %s\n" % tmp)

    def run(self):
        self.client = mqtt.Client(str(self.sid))
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        if self.username is not None and self.password is not None:
            self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.host, 1883, 60)
        self.client.loop_forever()

    def on_connect(self, client, obj, flags, rc):
        self.append_log(">> Connecting to MQTT server %s: %d" % (self.host, rc))
        for topic in self.topics:
            self.append_log(">> Subscribe topic: %s" % topic)
            self.client.subscribe(topic, qos=self.topic_qos)

    def on_message(self, client, obj, msg):
        self.arrived_msg = msg.payload.decode()
        self.append_log(self.arrived_msg)

    @staticmethod
    def timeStamp():
        return str(datetime.datetime.now())[:-5]

    def check_logfile_valid(self):
        if os.path.isfile(self.filename) is True:
            self.valid_logfile = True
        else:
            open(self.filename, 'a').close()
            self.valid_logfile = os.path.isfile(self.filename)
            if self.valid_logfile is True:
                msg = '>>Log file %s was created successfully' % self.filename
            else:
                msg = '>>Log file %s failed to create' % self.filename
            print(msg)
            self.append_log(msg)

    def append_log(self, log_entry=''):
        self.msg = '[%s] %s' % (self.timeStamp(), log_entry)

        if self.valid_logfile is True:
            myfile = open(self.filename, 'a')
            myfile.write(self.msg + '\n')
            myfile.close()
        else:
            print('Log err')
        if self.output2screen == 1:
            print(self.msg)


a = MQTTlogger(sid="MQTTlogger", topics=['HomePi/Dvir/Windows/All', 'HomePi/Dvir/Messages'], topic_qos=0)
a.start()

