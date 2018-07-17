import paho.mqtt.client as mqtt  # import the client1
import time


############
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_connect(client, userdata, flags, rc):
    # logging.info("Connected flags" + str(flags) + "result code " \
    #              + str(rc) + "client1_id ")
    print(flags, rc)
    client.connected_flag = True

def on_subscribe():
    print("HI")


# def on_connect(client, userdata):
#     pass

########################################


broker_address = "192.168.2.113"
broker_address = "iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("TEST1")  # create new instance
client.on_message = on_message  # attach function to callback
print("connecting to broker")
client.connect(broker_address)  # connect to broker
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.loop_start()  # start the loop
print("Subscribing to topic", "house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic", "house/bulbs/bulb1")
# client.publish("house/bulbs/bulb1", "OFF")
time.sleep(4)  # wait
client.loop_stop()  # stop the loop

# import paho.mqtt.client as mqtt
#
#
# class MqtComm:
#     def __init__(self, client_name=None):
#         self.client = mqtt.Client(client_name)
#
#         pass
#
#     def subscr(self, topic):
#         client.subscribe(topic)
#
#     def on_msg(self, self.client, userdata, msg):
#         print(msg.topic + " " + str(msg.payload))
#
#
#     # The callback for when the client receives a CONNACK response from the server.
#     def on_connect(client, userdata, flags, rc):
#         print("Connected with result code " + str(rc))
#
#         # Subscribing in on_connect() means that if we lose the connection and
#         # reconnect then subscriptions will be renewed.
#         # client.subscribe("$SYS/#")
#     client.subscribe("hello_dotty")
#
#
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))
#
#
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
#
# # client.connect("iot.eclipse.org", 1883, 60)
# client.connect('192.168.2.11', 1883, 60)
#
# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# client.loop_forever()
