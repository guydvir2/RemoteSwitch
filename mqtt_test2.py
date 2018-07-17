import mqtt_switch
import time

def f1():
    print("F1")


a = mqtt_switch.MQTTClient(topic='HomePi/dvir/test1', topic_qos=0, host='192.168.2.113')
a.commands({'rel1': 'on'})
a.start()
time.sleep(1)
a.pub("rel1")