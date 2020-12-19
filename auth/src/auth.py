from flask import Flask, request
from copy import deepcopy
import mysql.connector
import os
import json
import jwt

auth = Flask(__name__)

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

@auth.route('/login', methods = ['POST'])
def login():
	username = request.form.get('username')
	password = request.form.get('password')

	connect_to_db()
	cursor.callproc('check_user', [username, password])

	user_details = None

	for result in cursor.stored_results():
		user_details = result.fetchone()

	if not user_details:
		cursor.close()
		return "", 401

	user_id = user_details[0]
	role = user_details[1]
	cursor.close()
	
	encoded_jwt = jwt.encode({'role': role, 'user_id': user_id}, secret, algorithm='HS256')

	return encoded_jwt, 200

@auth.route('/users')
def get_users():
	connect_to_db()
	cursor.callproc('get_users', [])

	users = []

	for result in cursor.stored_results():
		users = result.fetchall()

	cursor.close()

	return json.dumps(users), 200

@auth.route('/decode')
def authorize_user():
	token = request.form.get('token')
	user_details = None

	try:
		user_details = jwt.decode(token, secret, algorithms=['HS256'])
	except:
		return "", 401

	return json.dumps(user_details), 200

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

	auth.run(host='0.0.0.0', port=os.getenv('PORT', 8004), debug=True)