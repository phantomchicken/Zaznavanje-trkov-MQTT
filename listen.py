import paho.mqtt.client as mqtt
from store import sensortag_handler
from store import mobitel_handler

MQTT_Broker = "192.168.22.61" #
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic = "/avtomobili/#" #poslušamo avtomobile vseh odjemalcev
MQTT_Username = "uporabnik3" #administratorski uporabnik
MQTT_Password = "geslo3"

#Subscribe to all Sensors at Base Topic
def on_connect(mosq, obj, rc):
	client.subscribe(MQTT_Topic, 0)

def on_message(mosq, obj, msg):
	if(len(msg.topic.split('/'))>3):	# ni tipa /avtomobili/uporabnik2")
		mobitel_handler(msg.topic, msg.payload.decode("utf-8"))		
	else:
		sensortag_handler(msg.topic, msg.payload.decode("utf-8"))
	

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

client = mqtt.Client()

# nastavitev odjemalca
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.username_pw_set(MQTT_Username, MQTT_Password)

# povezovanje
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# neskončna zanka
client.loop_forever()
