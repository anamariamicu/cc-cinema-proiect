from flask import Flask, request
from copy import deepcopy
import mysql.connector
import os
import json
import sys
import requests

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
url_auth = None

def token_required(func):
	def wrap():
		try:
			token_passed = request.headers['token']
		except:
			return "Token-ul este obligatoriu", 401
		if token_passed != '' and token_passed != None:
			url = url_auth + '/decode'
			data = {
				'token': token_passed
			}
			response = requests.get(url = url, data = data)

			if response.status_code == 401:
				return "Token invalid", 401

			user_details = response.json()
			user_id = user_details['user_id']
			role = user_details['role']

			if role != 1 and role != 0:
				return "Acces nepermis", 401

			return func()
		else:
			return "Token-ul este obligatoriu", 401

	wrap.__name__ = func.__name__
	return wrap

@server.route('/movie')
@token_required
def get_movies():
	connect_to_db()
	cursor.callproc('get_movies', [])

	movies = []

	for result in cursor.stored_results():
		movies = result.fetchall()

	cursor.close()

	return json.dumps(movies), 200

@server.route('/screening/movie')
@token_required
def get_screenings():
	movie_id = request.args.get('movie_id')

	connect_to_db()
	cursor.callproc('get_screenings', [movie_id])

	screenings = []

	for result in cursor.stored_results():
		screenings = result.fetchall()

	cursor.close()

	return json.dumps(screenings), 200

@server.route('/screening/date')
@token_required
def get_screenings_for_date():
	date = request.args.get('date')

	connect_to_db()
	cursor.callproc('get_screenings_for_date', [date])

	screenings = []

	for result in cursor.stored_results():
		screenings = result.fetchall()

	cursor.close()

	return json.dumps(screenings), 200

@server.route('/screening/cinema_hall')
@token_required
def get_seats_for_screening():
	screening_id = request.args.get('screening_id')

	connect_to_db()
	cursor.callproc('check_screening_exists', [screening_id])

	number_of_screenings = None
	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	cursor.close()

	if number_of_screenings == 0:
		return 'ID-ul proiectiei filmului este invalid', 410

	connect_to_db()
	cursor.callproc('get_seats_for_screening', [screening_id])

	seats_db = []

	for result in cursor.stored_results():
		seats_db = result.fetchall()

	cursor.close()

	connect_to_db()
	cursor.callproc('get_number_of_seats_for_screening', [screening_id])

	number_of_seats_db = None

	for result in cursor.stored_results():
		number_of_seats_db = result.fetchone()

	cursor.close()

	number_of_rows = number_of_seats_db[0]
	number_of_seats_per_row = number_of_seats_db[1]

	seats = [['L' for s in range(number_of_seats_per_row)] for r in range(number_of_rows)]

	for seat_db in seats_db:
		(row, number, purchased) = seat_db

		if purchased:
			seats[row - 1][number - 1] = 'C'
		else:
			seats[row - 1][number - 1] = 'R'

	return json.dumps(seats), 200

@server.route('/reservation', methods = ['POST'])
@token_required
def get_reservation():
	seats = request.form.getlist('seats')
	screening_id = request.form.get('screening_id')

	connect_to_db()
	cursor.callproc('check_screening', [screening_id])

	number_of_screenings = None

	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	if not number_of_screenings:
		cursor.close()
		return "", 410

	cursor.close()

	for index in range(int(len(seats) / 2)):
		seat = (seats[2 * index], seats[2 * index + 1])

		connect_to_db()
		cursor.callproc('check_seat', [screening_id, seat[0], seat[1]])

		number_of_seats = None

		for result in cursor.stored_results():
			number_of_seats = result.fetchone()[0]

		if number_of_seats == 0:
			cursor.close()
			return "", 402

		cursor.close()

		connect_to_db()
		cursor.callproc('check_seat_reserved', [screening_id, seat[0], seat[1]])

		number_of_seats = None

		for result in cursor.stored_results():
			number_of_seats = result.fetchone()[0]

		if number_of_seats != 0:
			cursor.close()
			return "", 403

		cursor.close()

	connect_to_db()
	cursor.callproc('add_reservation', [screening_id])

	for result in cursor.stored_results():
		id_reservation = result.fetchone()[0]

		cursor.close()

	for index in range(int(len(seats) / 2)):
		seat = (seats[2 * index], seats[2 * index + 1])

		connect_to_db()
		cursor.callproc('add_reserved_seat', [screening_id, id_reservation, seat[0], seat[1]])
		cursor.close()

	return str(id_reservation), 200

@server.route('/reservation/details')
@token_required
def get_reservation_details():
	reservation_id = request.args.get('reservation_id')

	connect_to_db()
	cursor.callproc('get_reservation_details', [reservation_id])

	reservation = []

	for result in cursor.stored_results():
		reservation = result.fetchall()[0]

	cursor.close()

	seats = []

	connect_to_db()
	cursor.callproc('get_seats_for_reservation', [reservation_id])

	for result in cursor.stored_results():
		seats = result.fetchall()

	cursor.close()

	purchased = reservation[5]
	reservation = list(reservation)
	reservation[5] = deepcopy(seats)
	reservation.append(purchased)

	print(reservation)

	return json.dumps(reservation), 200

@server.route('/reservation/remove', methods = ['POST'])
@token_required
def remove_reservation():
	id = request.form.get('id')

	connect_to_db()
	cursor.callproc('check_reservation', [id])

	number_of_reservations = None
	for result in cursor.stored_results():
		number_of_reservations = result.fetchone()[0]

	cursor.close()

	if number_of_reservations == 0:
		return '', 410

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
@token_required
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
		return '', 410

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
	if len(sys.argv) != 1:
		print('Mod de utilizare: python server.py')
		exit(1)

	url_auth = os.environ.get('URL_AUTH')

	if (url_auth == None):
		print('Variabila de mediu necesara: URL_AUTH')
		exit(1)

	server.run(host='0.0.0.0', port=os.getenv('PORT', 8002), debug=True)
