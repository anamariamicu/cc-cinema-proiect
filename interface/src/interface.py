import requests
import sys

headers = None

def print_menu():
	print('')
	print('Introduceti una dintre urmatoarele comenzi (numerice):')
	print('Logare in alt cont: 0')
	print('Afiseaza filmele disponibile: 1')
	print('Afiseaza proiectiile pentru un film: 2')
	print('Afiseaza proiectiile disponibile pentru o anumita zi: 3')
	print('Afiseaza situatia salii pentru o proiectie: 4')
	print('Realizeaza o rezervare: 5')
	print('Afiseaza detalii despre o rezervare: 6')
	print('Anuleaza o rezervare: 7')
	print('Achita o rezervare: 8')
	print('Adauga o sala de cinema: 9')
	print('Elimina o sala de cinema: 10')
	print('Afiseaza toate salile de cinema: 11')
	print('Adauga un film: 12')
	print('Elimina un film: 13')
	print('Adauga o proiectie a unui film: 14')
	print('Elimina o proiectie a unui film: 15')
	print('Afiseaza toate rezervarile pentru o proiectie a unui film: 16')
	print('Iesire: 17')

def print_login(url):
	global headers
	headers = None

	while headers == None:
		print('')
		username_auth = None
		password_auth = None

		while username_auth == None:
			print('Introduceti numele utilizatorului:')
			username = input()
			if username:
				username_auth = username
			else:
				print('Numele utilizatorului nu poate fi nul')
		while password_auth == None:
			print('Introduceti parola:')
			password = input()
			if password:
				password_auth = password
			else:
				print('Parola nu poate fi nula')

		current_url = url + '/auth/login'
		data = {
			'username': username_auth,
			'password': password_auth,
		}

		response = requests.post(url = current_url, data = data)

		if response.status_code == 200:
			print('Autentificare realizata cu succes')
			headers = {'token': response.text}
		else:
			print('Credentiale incorecte')

def print_movies(url):
	url = url + '/api/movie'
	response = requests.get(url = url, headers = headers)

	if response.status_code != 200:
		print(response.text)
		return

	movies = response.json()

	for movie in movies:
		print('')
		print('ID: ' + str(movie[0]))
		print('Nume: ' + movie[1])
		print('Gen: ' + movie[2])
		print('Durata (minute): ' + str(movie[3]))
		print('Descriere: ' + movie[4])

def print_screenings_for_movie(url):
	url = url + '/api/screening/movie'

	print('Introduceti ID-ul filmului:')

	movie_id = input()
	params = {
		'movie_id': movie_id,
	}

	response = requests.get(url = url, params = params, headers = headers)

	if response.status_code != 200:
		print(response.text)
		return

	screenings = response.json()

	for screening in screenings:
		print('')
		print('ID proiectie: ' + str(screening[0]))
		print('Data: ' + str(screening[2]))

def print_screenings_for_day(url):
	url = url + '/api/screening/date'

	print('Introduceti data sub urmatorul format YYYY-MM-DD:')

	date = input()
	params = {
		'date': date,
	}

	response = requests.get(url = url, params = params, headers = headers)

	if response.status_code != 200:
		print(response.text)
		return

	screenings = response.json()

	for screening in screenings:
		print('')
		print('ID proiectie: ' + str(screening[0]))
		print('Data: ' + str(screening[1]))
		print('Nume film: ' + screening[2])
		print('Gen film: ' + screening[3])
		print('Durata film (minute): ' + str(screening[4]))
		print('Descriere film: ' + screening[5])

def print_cinema_hall(url):
	url = url + '/api/screening/cinema_hall'

	print('Introduceti ID-ul proiectiei filmului:')

	screening_id = input()
	params = {
		'screening_id': screening_id,
	}

	response = requests.get(url = url, params = params, headers = headers)
	
	if response.status_code != 200:
		print(response.text)
		return

	# matrice cu loc liber/rezervat/cumparat
	result_matrix = response.json()

	for r in result_matrix:
		print(r)

def get_reservation(url):
	print('Introduceti datele sub urmatorul format:')
	print('ID_Proiectie#Rand,Loc#Rand,Loc...')

	info = input()
	info_array = info.split('#')

	if (len(info_array) < 2):
		print('Comanda invalida')
		return

	screening_id = info_array[0]
	seats = []

	for index in range(1, len(info_array)):
		seat = info_array[index]
		seats.append(seat.split(','))

	url = url + '/api/reservation'
	data = {
		'screening_id': screening_id,
		'seats': seats,
	}

	response = requests.post(url = url, data = data, headers = headers)

	if response.status_code != 200:
		if response.status_code == 410:
			print('Rezervare esuata (ID-ul proiectiei este invalid)')
		elif response.status_code == 402:
			print('Rezervare esuata (unul dintre locuri este invalid)')
		elif response.status_code == 403:
			print('Rezervare esuata (unul dintre locuri este rezervat/cumparat)')
		elif response.status_code == 401:
			print('Acces nepermis')
	else:
		print('Rezervare realizata cu succes. ID-ul rezervarii: ' + response.text)

def print_reservation(url):
	url = url + '/api/reservation/details'

	print('Introduceti ID-ul rezervarii:')

	reservation_id = input()
	params = {
		'reservation_id': int(reservation_id),
	}

	response = requests.get(url = url, params = params, headers = headers)

	if not response:
		print("ID-ul este invalid")
		return

	if response.status_code != 200:
		print(response.text)
		return

	reservation = response.json()

	print('ID rezervare: ' + str(reservation[0]))
	print('ID film: ' + str(reservation[1]))
	print('Nume film: ' + reservation[2])
	print('Data: ' + str(reservation[3]))
	print('Nume sala de cinema: ' + reservation[4])

	# reservation[6] - lista cu perechi de tipul (nr_rand, nr_loc)
	seats = ''
	for seat in reservation[5]:
		seats = seats + ' R' + str(seat[0]) + 'L' + str(seat[1])
	print('Locuri:' + seats)

	if reservation[6] == 1:
		print('Este cumparata: Da')
	else:
		print('Este cumparata: Nu')

def remove_reservation(url):
	url = url + '/api/reservation/remove'

	print('Introduceti ID-ul rezervarii:')

	reservation_id = input()
	data = {
		'id': int(reservation_id)
	}

	response = requests.post(url = url, data = data, headers = headers)

	if response.status_code != 200:
		if response.status_code == 410:
			print('Anularea rezervarii esuata (ID-ul rezervarii este invalid)')
		elif response.status_code == 402:
			print('Anularea rezervarii esuata (rezervarea este deja achitata)')
		elif response.status_code == 401:
			print('Acces nepermis')
	else:
		print('Anulare realizata cu succes')

def buy_reservation(url):
	print('Introduceti datele sub urmatorul format:')
	print('ID_rezervare#Informatii_card_credit')

	info = input()
	info_array = info.split('#')

	if (len(info_array) != 2):
		print('Comanda invalida')
		return

	url = url + '/api/reservation/buy'
	data = {
		'reservation_id': info_array[0],
		'credit_card_information': info_array[1]
	}

	response = requests.post(url = url, data = data, headers = headers)

	if response.status_code != 200:
		if response.status_code == 410:
			print('Cumparare esuata (ID-ul rezervarii este invalid)')
		elif response.status_code == 402:
			print('Cumparare esuata (rezervarea a fost deja achitata)')
		elif response.status_code == 401:
			print('Acces nepermis')
	else:
		print('Cumparare realizata cu succes')



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

	url = url + '/admin/cinema_hall/add'
	data = {
		'name': info_array[0],
		'number_of_rows': int(info_array[1]),
		'number_of_seats_per_row': int(info_array[2])
	}

	response = requests.post(url = url, data = data, headers = headers)
	print(response.text)

def remove_cinema_hall(url):
	print('Introduceti ID-ul salii de cinema:')
	cinema_hall_id = input()

	url = url + '/admin/cinema_hall/remove'
	data = {
		'id': int(cinema_hall_id)
	}

	response = requests.post(url = url, data = data, headers = headers)
	print(response.text)

def add_movie(url):
	print('Introduceti datele sub urmatorul format:')
	print('Nume#Gen#Durata_Min#Descriere')

	info = input()
	info_array = info.split('#')

	if (len(info_array) != 4):
		print('Comanda invalida')
		return

	url = url + '/admin/movie/add'
	data = {
		'name': info_array[0],
		'genre': info_array[1],
		'duration_minutes': int(info_array[2]),
		'description': info_array[3]
	}

	response = requests.post(url = url, data = data, headers = headers)
	print(response.text)

def remove_movie(url):
	print('Introduceti ID-ul filmului:')
	movie_id = input()

	url = url + '/admin/movie/remove'
	data = {
		'id': int(movie_id)
	}

	response = requests.post(url = url, data = data, headers = headers)
	print(response.text)

def add_screening(url):
	print('Introduceti datele sub urmatorul format:')
	print('ID_Film#ID_Sala#YYYY-MM-DD HH:MM:SS')

	info = input()
	info_array = info.split('#')

	if (len(info_array) != 3):
		print('Comanda invalida')
		return

	url = url + '/admin/screening/add'
	data = {
		'movie_id': int(info_array[0]),
		'cinema_hall_id': int(info_array[1]),
		'start_date': info_array[2]
	}

	response = requests.post(url = url, data = data, headers = headers)
	print(response.text)

def remove_screening(url):
	print('Introduceti ID-ul proiectiei fimului:')
	screening_id = input()

	url = url + '/admin/screening/remove'
	data = {
		'id': int(screening_id)
	}

	response = requests.post(url = url, data = data, headers = headers)
	print(response.text)

def print_reservations(url):
	url = url + '/admin/screening/reservations'

	print('Introduceti ID-ul proiectiei filmului:')

	screening_id = input()
	params = {
		'screening_id': screening_id,
	}

	response = requests.get(url = url, params = params, headers = headers)

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

def print_cinema_halls(url):
	url = url + '/admin/cinema_hall'
	response = requests.get(url = url, headers = headers)

	if response.status_code != 200:
		print(response.text)
		return

	cinema_halls = response.json()

	for cinema_hall in cinema_halls:
		print('')
		print('ID: ' + str(cinema_hall[0]))
		print('Nume: ' + cinema_hall[1])
		print('Numar de randuri: ' + str(cinema_hall[2]))
		print('Numar de locuri pe rand: ' + str(cinema_hall[3]))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Mod de utilizare: python interface.py *url_gateway*')
		exit(1)
	url = sys.argv[1]

	print_login(url)
	
	while True:
		print_menu()
		command = input()

		if command == '0':
			print_login(url)
		elif command == '1':
			print_movies(url)
		elif command == '2':
			print_screenings_for_movie(url)
		elif command == '3':
			print_screenings_for_day(url)
		elif command == '4':
			print_cinema_hall(url)
		elif command == '5':
			get_reservation(url)
		elif command == '6':
			print_reservation(url)
		elif command == '7':
			remove_reservation(url)
		elif command == '8':
			buy_reservation(url)
		elif command == '9':
			add_cinema_hall(url)
		elif command == '10':
			remove_cinema_hall(url)
		elif command == '11':
			print_cinema_halls(url)
		elif command == '12':
			add_movie(url)
		elif command == '13':
			remove_movie(url)
		elif command == '14':
			add_screening(url)
		elif command == '15':
			remove_screening(url)
		elif command == '16':
			print_reservations(url)
		elif command == '17':
			break
		else:
			print('Comanda invalida')