import paho.mqtt.client as mqtt
import time
import os

broker = "192.168.22.61"
port = 1883
username = "uporabnik3"
password = "geslo3"

def on_connect(mosq, obj, rc):
	client.subscribe('#', 0)
	client.subscribe('$SYS/#')

def on_message(client, userdata, message):
	print('Tema: %s | QOS: %s  | Besedilo: %s' % (message.topic, message.qos, message.payload))


client = mqtt.Client()
client.username_pw_set(username="uporabnik3", password="geslo3")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 45)
client.loop_forever()