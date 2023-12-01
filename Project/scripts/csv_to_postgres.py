import os
import pandas as pd
import psycopg2
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
	print('Connected with result code '+str(rc))
	client.subscribe('csv_topic')

def on_message(client, userdata, msg):
	# Procesar el archivo CSV
	csv_filename = msg.payload.decode('utf-8')
	df = pd.read_csv(csv_filename)

	# Conectar a PostgreSQL
	conn = psycopg2.connect(
		database='your_database_name',
		user='your_username',
		password='your_password',
		host='postgres',
		port='5432'
	)

	# Cargar datos en la tabla existente
	df.to_sql('your_table_name', conn, if_exists='replace', index=False)

	conn.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('mqtt-broker', 1883, 60)

client.loop_start()

while True:
	# Escanear la carpeta cada 5 minutos
	for filename in os.listdir('csv_folder'):
		if filename.endswith('.csv'):
			client.publish('csv_topic', os.path.join('csv_folder', filename))
			time.sleep(1)  # Esperar un segundo entre mensajes para evitar congestionar el sistema

	time.sleep(300)  # Esperar 5 minutos antes de volver a escanear la carpeta

import socket

try:
	socket.gethostbyname('mqtt-broker')
except socket.gaierror as e:
	print(f'Error al resolver el nombre del host: {e}')
