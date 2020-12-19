import requests
import sys

def print_menu():
	print('')
	print('Introduceti una dintre urmatoarele comenzi (numerice):')
	print('Afiseaza filmele disponibile: 1')
	print('Afiseaza proiectiile pentru un film: 2')
	print('Afiseaza proiectiile disponibile pentru o anumita zi: 3')
	print('Afiseaza situatia salii pentru o proiectie: 4')
	print('Realizeaza o rezervare: 5')
	print('Afiseaza detalii despre o rezervare: 6')
	print('Anuleaza o rezervare: 7')
	print('Achita o rezervare: 8')
	print('Iesire: 9')

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

def print_screenings_for_movie(url):
	url = url + '/screening/movie'

	print('Introduceti ID-ul filmului:')

	movie_id = input()
	params = {
		'movie_id': movie_id,
	}

	response = requests.get(url = url, params = params)
	screenings = response.json()

	for screening in screenings:
		print('')
		print('ID proiectie: ' + str(screening[0]))
		print('Data: ' + str(screening[2]))

def print_screenings_for_day(url):
	url = url + '/screening/date'

	print('Introduceti data sub urmatorul format YYYY-MM-DD:')

	date = input()
	params = {
		'date': date,
	}

	response = requests.get(url = url, params = params)
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

	url = url + '/reservation'
	data = {
		'screening_id': screening_id,
		'seats': seats,
	}

	response = requests.post(url = url, data = data)

	if not response.text:
		if response.status_code == 401:
			print('Rezervare esuata (ID-ul proiectiei este invalid)')
		elif response.status_code == 402:
			print('Rezervare esuata (unul dintre locuri este invalid)')
		elif response.status_code == 403:
			print('Rezervare esuata (unul dintre locuri este rezervat/cumparat)')
	else:
		print('Rezervare realizata cu succes. ID-ul rezervarii: ' + response.text)

def print_reservation(url):
	url = url + '/reservation/details'

	print('Introduceti ID-ul rezervarii:')

	reservation_id = input()
	params = {
		'reservation_id': int(reservation_id),
	}

	response = requests.get(url = url, params = params)

	if not response:
		print("ID-ul este invalid")
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
	url = url + '/reservation/remove'

	print('Introduceti ID-ul rezervarii:')

	reservation_id = input()
	data = {
		'id': int(reservation_id)
	}

	response = requests.post(url = url, data = data)

	if not response.text:
		if response.status_code == 401:
			print('Anularea rezervarii esuata (ID-ul rezervarii este invalid)')
		elif response.status_code == 402:
			print('Anularea rezervarii esuata (rezervarea este deja achitata)')
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

	url = url + '/reservation/buy'
	data = {
		'reservation_id': info_array[0],
		'credit_card_information': info_array[1]
	}

	response = requests.post(url = url, data = data)

	if not response.text:
		if response.status_code == 401:
			print('Cumparare esuata (ID-ul rezervarii este invalid)')
		elif response.status_code == 402:
			print('Cumparare esuata (rezervarea a fost deja achitata)')
	else:
		print('Cumparare realizata cu succes')

if __name__ == '__main__':
	while True:
		if len(sys.argv) != 2:
			print('Mod de utilizare: python client.py *url_server*')
			exit(1)
		url = sys.argv[1]

		print_menu()
		command = input()

		if command == '1':
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
			break
		else:
			print('Comanda invalida')