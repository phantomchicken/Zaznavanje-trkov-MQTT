import sqlite3

ukaz="""

drop table if exists SensorTag ;
create table SensorTag (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  acc_x integer,
  acc_y integer,
  acc_z integer,
  air_pressure integer,
  ambient_temp integer,
  compass_x integer,
  compass_y integer,
  compass_z integer,
  gyro_x integer,
  gyro_y integer,
  gyro_z integer,
  humidity integer,
  key_1 integer,
  key_2 integer,
  light integer,
  reed_relay integer
);

drop table if exists Mobitel ;
create table Mobitel (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Accelerometer_x integer,
  Accelerometer_y integer,
  Accelerometer_z integer,
  Gyroscope_x integer,
  Gyroscope_y integer,
  Gyroscope_z integer,
  Gravity_x integer,
  Gravity_y integer,
  Gravity_z integer,
  Proximity_x integer,
  Proximity_y integer,
  Proximity_z integer,
  LinearAcceleration_x integer,
  LinearAcceleration_y integer,
  LinearAcceleration_z integer,
  RotationVector_x integer,
  RotationVector_y integer,
  RotationVector_z integer,
  LightIntensity_x integer,
  LightIntensity_y integer,
  LightIntensity_z integer,
  noise_decibels text
);

"""

conn = sqlite3.connect("MQTT_veriga.db")
cursor = conn.cursor()

sqlite3.complete_statement(ukaz)
cursor.executescript(ukaz)

cursor.close()
conn.close()