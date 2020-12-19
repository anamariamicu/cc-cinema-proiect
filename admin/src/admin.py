from flask import Flask, request, Response
import mysql.connector
import os
import json

admin = Flask(__name__)

config = {
	'user': 'root',
	'password': 'rootpass',
	'host': 'db',
	'port': '3306',
	'database': 'cinema_service'
}

cursor = None
connection = None

@admin.route('/cinema_hall/add', methods = ['POST'])
def add_cinema_hall():
	name = request.form.get('name')
	number_of_rows = request.form.get('number_of_rows')
	number_of_seats_per_row = request.form.get('number_of_seats_per_row')

	if 	not name or not number_of_rows or not number_of_seats_per_row:
		return 'Sala de cinema nu a putut fi adaugata (parametri invalizi)', 401

	connect_to_db()
	cursor.callproc('add_cinema_hall', [name, number_of_rows, number_of_seats_per_row])
	cursor.close()

	return 'Sala de cinema adaugata cu succes', 200

@admin.route('/cinema_hall')
def get_cinema_halls():
	connect_to_db()
	cursor.callproc('get_cinema_halls', [])

	cinema_halls = []

	for result in cursor.stored_results():
		cinema_halls = result.fetchall()

	cursor.close()

	return json.dumps(cinema_halls), 200

@admin.route('/cinema_hall/remove', methods = ['POST'])
def remove_cinema_hall():
	id = request.form.get('id')

	connect_to_db()
	cursor.callproc('check_cinema_hall_exists', [id])

	number_of_cinema_halls = None
	for result in cursor.stored_results():
		number_of_cinema_halls = result.fetchone()[0]

	cursor.close()

	if number_of_cinema_halls == 0:
		return 'Sala de cinema nu poate fi eliminata (ID invalid)', 401

	connect_to_db()
	cursor.callproc('check_cinema_hall', [id])

	number_of_screenings = None
	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	cursor.close()

	if number_of_screenings != 0:
		return 'Sala de cinema nu poate fi eliminata (exista proiectii de film programate)', 402

	connect_to_db()
	cursor.callproc('remove_cinema_hall', [id])
	cursor.close()

	return 'Sala de cinema eliminata cu succes', 200

@admin.route('/movie/add', methods = ['POST'])
def add_movie():
	name = request.form.get('name')
	genre = request.form.get('genre')
	duration_minutes = request.form.get('duration_minutes')
	description = request.form.get('description')

	if 	not name or not genre or not duration_minutes or not description:
		return 'Filmul nu a putut fi adaugat (parametri invalizi)', 401

	connect_to_db()
	cursor.callproc('add_movie', [name, genre, duration_minutes, description])
	cursor.close()

	return 'Film adaugat cu succes', 200

@admin.route('/movie')
def get_movies():
	connect_to_db()
	cursor.callproc('get_movies', [])

	movies = []

	for result in cursor.stored_results():
		movies = result.fetchall()

	cursor.close()

	return json.dumps(movies), 200

@admin.route('/movie/remove', methods = ['POST'])
def remove_movie():
	id = request.form.get('id')

	connect_to_db()
	cursor.callproc('check_movie_exists', [id])

	number_of_movies = None
	for result in cursor.stored_results():
		number_of_movies = result.fetchone()[0]

	cursor.close()

	if number_of_movies == 0:
		return 'Filmul nu poate fi eliminat (ID invalid)', 401
		
	connect_to_db()
	cursor.callproc('check_movie', [id])

	number_of_screenings = None
	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	cursor.close()

	if number_of_screenings != 0:
		return 'Filmul nu poate fi eliminat (exista proiectii de film programate)', 402
		
	connect_to_db()
	cursor.callproc('remove_movie', [id])
	cursor.close()

	return 'Film eliminat cu succes', 200

@admin.route('/screening/add', methods = ['POST'])
def add_screening():
	movie_id = request.form.get('movie_id')
	cinema_hall_id = request.form.get('cinema_hall_id')
	start_date = request.form.get('start_date')

	if 	not movie_id or not cinema_hall_id or not start_date:
		return 'Proiectia filmului nu a putut fi adaugata (parametri invalizi)', 401

	connect_to_db()
	cursor.callproc('add_screening', [movie_id, cinema_hall_id, start_date])
	cursor.close()

	return 'Proiectia filmului adaugata cu succes', 200

@admin.route('/screening')
def get_screenings():
	movie_id = request.args.get('movie_id')

	connect_to_db()
	cursor.callproc('get_screenings', [movie_id])

	screenings = []

	for result in cursor.stored_results():
		screenings = result.fetchall()

	cursor.close()

	return json.dumps(screenings), 200

@admin.route('/screening/remove', methods = ['POST'])
def remove_screening():
	id = request.form.get('id')

	connect_to_db()
	cursor.callproc('check_screening_exists', [id])

	number_of_screenings = None
	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	cursor.close()

	if number_of_screenings == 0:
		return 'Proiectia nu poate fi eliminata (ID invalid)', 401

	connect_to_db()
	cursor.callproc('check_screening', [id])

	number_of_reservations = None
	for result in cursor.stored_results():
		number_of_reservations = result.fetchone()[0]

	cursor.close()

	if number_of_reservations != 0:
		return 'Proiectia filmului nu poate fi eliminat (exista bilete rezervate/cumparate)', 402
		
	connect_to_db()
	cursor.callproc('remove_screening', [id])
	cursor.close()

	return 'Proiectia filmului eliminata cu succes', 200

@admin.route('/screening/cinema_hall')
def get_seats_for_screening():
	screening_id = request.args.get('screening_id')

	connect_to_db()
	cursor.callproc('check_screening_exists', [screening_id])

	number_of_screenings = None
	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	cursor.close()

	if number_of_screenings == 0:
		return 'ID-ul proiectiei filmului este invalid', 401

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

@admin.route('/screening/reservations')
def get_reservations():
	screening_id = request.args.get('screening_id')

	connect_to_db()
	cursor.callproc('check_screening_exists', [screening_id])

	number_of_screenings = None
	for result in cursor.stored_results():
		number_of_screenings = result.fetchone()[0]

	cursor.close()

	if number_of_screenings == 0:
		return 'ID-ul proiectiei filmului este invalid', 401

	connect_to_db()
	cursor.callproc('get_reservations', [screening_id])

	reservations_db = []
	reservations = {}

	for result in cursor.stored_results():
		reservations_db = result.fetchall()

	cursor.close()

	for r in reservations_db:
		(id, row, seat_number, purchased, credit_card_info) = r

		if id in reservations:
			reservations[id][1].append((row, seat_number))
		else:
			reservations[id] = (id, [(row, seat_number)], purchased, credit_card_info)

	return json.dumps(list(reservations.values())), 200

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

	admin.run(host='0.0.0.0', port=os.getenv('PORT', 8000), debug=True)
