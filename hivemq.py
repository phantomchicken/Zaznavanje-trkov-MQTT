import paho.mqtt.client as mqtt

def interrupt(topic):
	MQTT_Broker = "7db78138fe46481fac320cc9911d3275.s1.eu.hivemq.cloud" #
	MQTT_Port = 8883
	Keep_Alive_Interval = 45
	MQTT_Username = "ninobrezac"
	MQTT_Password = "Test1234"

	def on_connect(mosq, obj, rc):
		client.subscribe(topic,0)

	# izpis sporocila v konzolo
	def on_message(mosq, obj, msg):
		print ("MQTT Data Received...")
		print ("MQTT Topic: " + msg.topic +" " +msg.payload.decode("utf-8"))
		

	def on_subscribe(mosq, obj, mid, granted_qos):
	    pass

	client = mqtt.Client()

	# nastavitev odjemalca
	client.on_message = on_message
	client.on_connect = on_connect
	client.on_subscribe = on_subscribe
	client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
	client.username_pw_set(MQTT_Username, MQTT_Password)

	# povezovanje
	client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

	# izpis nevarnosti v konzoli, posredovanje opozorila posredniku
	print("Zaznana nevarnost v " + topic)
	print(topic.split('/')[2])
	client.publish(topic, "Potencialna nevarnost pri " + topic.split('/')[2] + "!")

