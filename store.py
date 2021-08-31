import json
import sqlite3
from hivemq import interrupt

from datetime import datetime

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect("MQTT_veriga.db")
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

# zacetne vrednosti slovarja in ziroskopa
d2 = {}
gx = 0
gy = 0
gz = 0

def sensortag_handler(Topic, jsonData):
	json_Dict = json.loads(jsonData)
	d = json_Dict['d']

	# preskoci prvo sporocilo, ki vsebuje ime senzorja	
	if 'acc_x' in d:
		print (d)

		# priredi vse vrednosti senzorjev
		acc_x = d['acc_x']
		acc_y = d['acc_y']
		acc_z = d['acc_z']
		air_pressure = d['air_pressure']
		ambient_temp = d['ambient_temp']
		compass_x = d['compass_x']
		compass_y =d['compass_y']
		compass_z = d['compass_z']
		gyro_x = d['gyro_x']
		gyro_y = d['gyro_y']
		gyro_z = d['gyro_z']
		
		# doloci globalni kontekst za vrednosti ziroskopa
		global gx, gy, gz

		# ce je razlika prejsnje in trenutne vrednosti precejsnja, sprozi prekinitev in posodobi vrednosti		
		if (abs(gx-float(gyro_x))>=100 or abs(gy-float(gyro_y))>=100 or abs(gz-float(gyro_z))>=100):
			interrupt(Topic)
			gx = float(gyro_x)
			gy = float(gyro_y)
			gz = float(gyro_z)
	
		humidity = d['humidity']
		key_1 = d['key_1']
		key_2 = d['key_2']
		light = d['light']
		reed_relay = d['reed_relay']
		dbObj = DatabaseManager()

		# vstavi vrednosti v podatkovno bazo
		dbObj.add_del_update_db_record("insert into SensorTag (SensorID, Date_n_Time, acc_x, acc_y, acc_z, air_pressure, ambient_temp, compass_x, compass_y, compass_z, gyro_x, gyro_y, gyro_z, humidity, key_1, key_2, light, reed_relay) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",["senzor", (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f"), acc_x, acc_y, acc_z, air_pressure, ambient_temp, compass_x, compass_y, compass_z, gyro_x, gyro_y, gyro_z, humidity, key_1, key_2, light, reed_relay])		
		del dbObj


def mobitel_handler(Topic, jsonData):
	# doloci za katero vrednost se gre, in zapisi v slovar pod tim kljucem
	# primer vrednosti senzorja /avtomobili/uporabnik2/accelerometer/x
	# temo razdelimo po posevnici, kljuc sestavljata zadnja dva niza
	split = Topic.split('/')	
	key = split[3] + "_" + split [4]
	d2[key] = jsonData

	if (len(split)==5 and split[3] == "Gyroscope"):
		# doloci globalni kontekst za vrednosti ziroskopa
		global gx, gy, gz

		# ce je razlika prejsnje in trenutne vrednosti precejsnja, sprozi prekinitev in posodobi vrednosti		
		if (split[4]=="x" and abs(gx-float(jsonData))>=10) :
			interrupt(Topic)
			gx = float(jsonData)
		elif (split[4]=="y" and abs(gy-float(jsonData))>=10):
			interrupt(Topic)
			gy = float(jsonData)
		elif (split[4]=="z" and abs(gz-float(jsonData))>=10):
			interrupt(Topic)
			gz = float(jsonData)			
	# ce je vrednost hrup v decibelih, dobili smo zadnjo meritev zapisemo vrednosti v bazo
	
	if (len(split)==5 and split[1]=="avtomobili" and split[3] =="noise" and split[4]=="decibels"):	
		dbObj = DatabaseManager()
		dbObj.add_del_update_db_record("insert into Mobitel (SensorID, Date_n_Time, Accelerometer_x, Accelerometer_y, Accelerometer_z, \
Gyroscope_x, Gyroscope_y, Gyroscope_z, Gravity_x, Gravity_y, Gravity_z, Proximity_x, \
Proximity_y, Proximity_z, LinearAcceleration_x, LinearAcceleration_y, LinearAcceleration_z, RotationVector_x, RotationVector_y, \
RotationVector_z, LightIntensity_x, LightIntensity_y, LightIntensity_z, noise_decibels) \
 values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",["Mobitel",(datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f"), \
d2['Accelerometer_x'], d2['Accelerometer_y'], d2['Accelerometer_z'], d2['Gyroscope_x'], d2['Gyroscope_y'], d2['Gyroscope_z'], \
d2['Gravity_x'], d2['Gravity_y'], d2['Gravity_z'], d2['Proximity_x'], \
d2['Proximity_y'], d2['Proximity_z'], d2['LinearAcceleration_x'], d2['LinearAcceleration_y'], d2['LinearAcceleration_z'], \
d2['RotationVector_x'], d2['RotationVector_y'], d2['RotationVector_z'], d2['LightIntensity_x'], d2['LightIntensity_y'], d2['LightIntensity_z'], d2['noise_decibels']])
		del dbObj
