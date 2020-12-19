from flask import Flask, request
from copy import deepcopy
import mysql.connector
import os
import json
import jwt

server = Flask(__name__)

config = {
	'user': 'root',
	'password': 'rootpass',
	'host': 'db',
	'port': '3306',
	'database': 'cinema_service'
}

cursor = None
connection = None
secret = 'secret'

@server.route('/login', methods = ['POST'])
def login():
	username = request.form.get('username')
	password = request.form.get('password')

	connect_to_db()
	cursor.callproc('check_user', [username, password])

	role = None

	for result in cursor.stored_results():
		role = result.fetchone()[0]

	if not role:
		cursor.close()
		return "", 401

	cursor.close()
	
	encoded_jwt = jwt.encode({'role': role}, secret, algorithm='HS256')

	return encoded_jwt, 200

@server.route('/reservation/remove', methods = ['POST'])
def remove_reservation():
	id = request.form.get('id')

	connect_to_db()
	cursor.callproc('check_reservation', [id])

	number_of_reservations = None
	for result in cursor.stored_results():
		number_of_reservations = result.fetchone()[0]

	cursor.close()

	if number_of_reservations == 0:
		return '', 401

	connect_to_db()
	cursor.callproc('check_reservation_purchased', [id])

	purchased = None
	for result in cursor.stored_results():
		purchased = result.fetchone()[0]

	cursor.close()

	if purchased == 1:
		return '', 402
		
	connect_to_db()
	cursor.callproc('remove_reservation', [id])
	cursor.close()

	return "OK", 200

@server.route('/reservation/buy', methods = ['POST'])
def buy_reservation():
	id = request.form.get('reservation_id')
	credit_card_info = request.form.get('credit_card_information')

	connect_to_db()
	cursor.callproc('check_reservation', [id])

	number_of_reservations = None
	for result in cursor.stored_results():
		number_of_reservations = result.fetchone()[0]

	cursor.close()

	if number_of_reservations == 0:
		return '', 401

	connect_to_db()
	cursor.callproc('check_reservation_purchased', [id])

	purchased = None
	for result in cursor.stored_results():
		purchased = result.fetchone()[0]

	cursor.close()

	if purchased == 1:
		return '', 402
		
	connect_to_db()
	cursor.callproc('buy_reservation', [id, credit_card_info])
	cursor.close()

	return "OK", 200


def connect_to_db():
	global connection
	global cursor

	connected = None

	while not connected:
		try:
			connection = mysql.connector.connect(**config)
			cursor = connection.cursor()
			connected = True
		except:
			connected = False

if __name__ == '__main__':
	connect_to_db()
	cursor.close()

	server.run(host='0.0.0.0', port=os.getenv('PORT', 8004), debug=True)