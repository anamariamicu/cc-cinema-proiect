import requests
import sys

def print_menu():
	print('')
	print('Introduceti una dintre urmatoarele comenzi (numerice):')
	print('Adauga o sala de cinema: 1')
	print('Elimina o sala de cinema: 2')
	print('Afiseaza toate salile de cinema: 3')
	print('Adauga un film: 4')
	print('Elimina un film: 5')
	print('Afiseaza toate filmele: 6')
	print('Adauga o proiectie a unui film: 7')
	print('Elimina o proiectie a unui film: 8')
	print('Afiseaza toate proiectiile unui film: 9')
	print('Afiseaza situatia salii pentru o proiectie a unui film: 10')
	print('Afiseaza toate rezervarile pentru o proiectie a unui film: 11')
	print('Iesire: 12')

def add_cinema_hall(url):
	print('Introduceti datele sub urmatorul format:')
	print('Nume#Nr_Randuri#Nr_Locuri_Per_Rand')

	info = input()
	info_array = info.split('#')
	int_seats = []
	seats_number = 0

	if (len(info_array) != 3):
		print('Comanda invalida')
		return

	url = url + '/cinema_hall/add'
	data = {
		'name': info_array[0],
		'number_of_rows': int(info_array[1]),
		'number_of_seats_per_row': int(info_array[2])
	}

	response = requests.post(url = url, data = data)
	print(response.text)

def remove_cinema_hall(url):
	print('Introduceti ID-ul salii de cinema:')
	cinema_hall_id = input()

	url = url + '/cinema_hall/remove'
	data = {
		'id': int(cinema_hall_id)
	}

	response = requests.post(url = url, data = data)
	print(response.text)

def print_cinema_halls(url):
	url = url + '/cinema_hall'
	response = requests.get(url = url)
	cinema_halls = response.json()

	for cinema_hall in cinema_halls:
		print('')
		print('ID: ' + str(cinema_hall[0]))
		print('Nume: ' + cinema_hall[1])
		print('Numar de randuri: ' + str(cinema_hall[2]))
		print('Numar de locuri pe rand: ' + str(cinema_hall[3]))

def add_movie(url):
	print('Introduceti datele sub urmatorul format:')
	print('Nume#Gen#Durata_Min#Descriere')

	info = input()
	info_array = info.split('#')

	if (len(info_array) != 4):
		print('Comanda invalida')
		return

	url = url + '/movie/add'
	data = {
		'name': info_array[0],
		'genre': info_array[1],
		'duration_minutes': int(info_array[2]),
		'description': info_array[3]
	}

	response = requests.post(url = url, data = data)
	print(response.text)

def remove_movie(url):
	print('Introduceti ID-ul filmului:')
	movie_id = input()

	url = url + '/movie/remove'
	data = {
		'id': int(movie_id)
	}

	response = requests.post(url = url, data = data)
	print(response.text)

def print_movies(url):
	url = url + '/movie'
	response = requests.get(url = url)
	movies = response.json()

	for movie in movies:
		print('')
		print('ID: ' + str(movie[0]))
		print('Nume: ' + movie[1])
		print('Gen: ' + movie[2])
		print('Durata (minute): ' + str(movie[3]))
		print('Descriere: ' + movie[4])

def add_screening(url):
	print('Introduceti datele sub urmatorul format:')
	print('ID_Film#ID_Sala#YYYY-MM-DD HH:MM:SS')

	info = input()
	info_array = info.split('#')

	if (len(info_array) != 3):
		print('Comanda invalida')
		return

	url = url + '/screening/add'
	data = {
		'movie_id': int(info_array[0]),
		'cinema_hall_id': int(info_array[1]),
		'start_date': info_array[2]
	}

	response = requests.post(url = url, data = data)
	print(response.text)

def remove_screening(url):
	print('Introduceti ID-ul proiectiei fimului:')
	screening_id = input()

	url = url + '/screening/remove'
	data = {
		'id': int(screening_id)
	}

	response = requests.post(url = url, data = data)
	print(response.text)

def print_screenings(url):
	url = url + '/screening'

	print('Introduceti ID-ul filmului:')

	movie_id = input()
	params = {
		'movie_id': movie_id,
	}

	response = requests.get(url = url, params = params)
	screenings = response.json()

	for screening in screenings:
		print('')
		print('ID: ' + str(screening[0]))
		print('ID sala de cinema: ' + str(screening[1]))
		print('Data: ' + str(screening[2]))

def print_seats_for_screening(url):
	url = url + '/screening/cinema_hall'

	print('Introduceti ID-ul proiectiei filmului:')

	screening_id = input()
	params = {
		'screening_id': screening_id,
	}

	response = requests.get(url = url, params = params)

	if response.status_code != 200:
		print(response.text)
		return

	# matrice cu loc liber/rezervat/cumparat
	result_matrix = response.json()

	for r in result_matrix:
		print(r)

def print_reservations(url):
	url = url + '/screening/reservations'

	print('Introduceti ID-ul proiectiei filmului:')

	screening_id = input()
	params = {
		'screening_id': screening_id,
	}

	response = requests.get(url = url, params = params)

	if response.status_code != 200:
		print(response.text)
		return

	reservations = response.json()

	for reservation in reservations:
		print('')
		print('ID: ' + str(reservation[0]))
		# reservation[1] - lista cu perechi de tipul (nr_rand, nr_loc)
		seats = ''
		for seat in reservation[1]:
			seats = seats + ' R' + str(seat[0]) + 'L' + str(seat[1])
		print('Locuri:' + seats)

		if reservation[2] == 1:
			print('Este cumparata: Da')
			print('Informatii card de credit: ' + reservation[3])
		else:
			print('Este cumparata: Nu')

if __name__ == '__main__':
	while True:
		if len(sys.argv) != 2:
			print('Mod de utilizare: python admin-interface.py *url_admin*')
			exit(1)
		url = sys.argv[1]

		print_menu()
		command = input()

		if command == '1':
			add_cinema_hall(url)
		elif command == '2':
			remove_cinema_hall(url)
		elif command == '3':
			print_cinema_halls(url)
		elif command == '4':
			add_movie(url)
		elif command == '5':
			remove_movie(url)
		elif command == '6':
			print_movies(url)
		elif command == '7':
			add_screening(url)
		elif command == '8':
			remove_screening(url)
		elif command == '9':
			print_screenings(url)
		elif command == '10':
			print_seats_for_screening(url)
		elif command == '11':
			print_reservations(url)
		elif command == '12':
			break
		else:
			print('Comanda invalida')
