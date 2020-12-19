DROP DATABASE IF EXISTS cinema_service;
CREATE DATABASE cinema_service;

USE cinema_service;

DELIMITER ;

CREATE TABLE movie(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255),
	genre VARCHAR(255),
	duration_minutes INT,
	description VARCHAR(255)
);

CREATE TABLE cinema_hall(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255),
	number_of_rows INT,
	number_of_seats_per_row INT
);

CREATE TABLE user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255),
    user_password VARCHAR(255),
    user_role INT
);

CREATE TABLE screening(
	id INT AUTO_INCREMENT PRIMARY KEY,
	movie_id INT,
	cinema_hall_id INT,
	start_date DATETIME,
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (cinema_hall_id) REFERENCES cinema_hall(id)
);

CREATE TABLE seat(
	id INT AUTO_INCREMENT PRIMARY KEY,
	cinema_hall_id INT,
	row INT,
	number_seat INT,
	FOREIGN KEY (cinema_hall_id) REFERENCES cinema_hall(id)
);

CREATE TABLE reservation(
	id INT AUTO_INCREMENT PRIMARY KEY,
	screening_id INT,
	purchased INT,
	credit_card_info VARCHAR(255),
	time_of_reservation TIMESTAMP,
	FOREIGN KEY (screening_id) REFERENCES screening(id)
);

CREATE TABLE reserved_seat(
	id INT AUTO_INCREMENT PRIMARY KEY,
	seat_id INT,
	reservation_id INT,
	FOREIGN KEY (seat_id) REFERENCES seat(id),
	FOREIGN KEY (reservation_id) REFERENCES reservation(id)
);

DELIMITER //

DROP PROCEDURE IF EXISTS add_cinema_hall //
CREATE PROCEDURE add_cinema_hall(IN name_hall VARCHAR(256), IN rows INT, IN seats_per_row INT)
BEGIN
	INSERT INTO cinema_hall(name, number_of_rows, number_of_seats_per_row)
	VALUES (name_hall, rows, seats_per_row);
	COMMIT;
END //

DROP TRIGGER IF EXISTS add_seats_new_cinema_hall //
CREATE TRIGGER add_seats_new_cinema_hall
    AFTER INSERT ON cinema_hall
    FOR EACH ROW 
BEGIN
	DECLARE r INT;
	DECLARE s INT;
	SET r = new.number_of_rows;
	SET s = new.number_of_seats_per_row;

	REPEAT
		SET s = new.number_of_seats_per_row;
		REPEAT
    		INSERT INTO seat (cinema_hall_id, row, number_seat)
			VALUES (new.id, r, s);
			SET s = s - 1;
			UNTIL s <= 0
		END REPEAT;
		SET r = r - 1;
		UNTIL r <= 0
	END REPEAT;
END //

DROP TRIGGER IF EXISTS remove_reserved_seats //
CREATE TRIGGER remove_reserved_seats
    BEFORE DELETE ON reservation
    FOR EACH ROW 
BEGIN
	DELETE FROM reserved_seat
	WHERE reservation_id = old.id;
END //

DROP PROCEDURE IF EXISTS check_seat //
CREATE PROCEDURE check_seat(IN id_screening INT, IN row_number INT, IN seat_number INT)
BEGIN
	SELECT COUNT(*)
	FROM seat s, screening sc, cinema_hall c
	WHERE sc.id = id_screening AND
		  c.id = sc.cinema_hall_id AND
		  s.cinema_hall_id = c.id AND
		  s.row = row_number AND s.number_seat = seat_number;
END //

DROP PROCEDURE IF EXISTS check_seat_reserved //
CREATE PROCEDURE check_seat_reserved(IN id_screening INT, IN row_number INT, IN seat_number INT)
BEGIN
	SELECT COUNT(*)
	FROM seat s, screening sc, reservation r, reserved_seat rs
	WHERE sc.id = id_screening AND
		  r.screening_id = sc.id AND
		  rs.reservation_id = r.id AND
		  rs.seat_id = s.id AND
		  s.row = row_number AND s.number_seat = seat_number;
END //

DROP PROCEDURE IF EXISTS get_cinema_halls //
CREATE PROCEDURE get_cinema_halls()
BEGIN
	SELECT id, name, number_of_rows, number_of_seats_per_row
	FROM cinema_hall
	ORDER BY id;
END //

DROP PROCEDURE IF EXISTS check_cinema_hall //
CREATE PROCEDURE check_cinema_hall(IN id_hall INT)
BEGIN
	SELECT COUNT(*)
	FROM screening
	WHERE cinema_hall_id = id_hall;
END //

DROP PROCEDURE IF EXISTS check_cinema_hall_exists //
CREATE PROCEDURE check_cinema_hall_exists(IN id_hall INT)
BEGIN
	SELECT COUNT(*)
	FROM cinema_hall
	WHERE id = id_hall;
END //

DROP PROCEDURE IF EXISTS remove_cinema_hall //
CREATE PROCEDURE remove_cinema_hall(IN id_hall INT)
BEGIN
	DELETE FROM cinema_hall
	WHERE id = id_hall;
	COMMIT;
END //

DROP TRIGGER IF EXISTS remove_seats_remove_cinema_hall //
CREATE TRIGGER remove_seats_remove_cinema_hall
    BEFORE DELETE ON cinema_hall
    FOR EACH ROW 
BEGIN
	DELETE FROM seat
	WHERE cinema_hall_id = old.id;
END //

DROP PROCEDURE IF EXISTS add_movie //
CREATE PROCEDURE add_movie(IN name_movie VARCHAR(256), IN genre_movie VARCHAR(255), IN duration_minutes_movie INT, IN description_movie VARCHAR(255))
BEGIN
	INSERT INTO movie(name, genre, duration_minutes, description)
	VALUES (name_movie, genre_movie, duration_minutes_movie, description_movie);
	COMMIT;
END //

DROP PROCEDURE IF EXISTS get_movies //
CREATE PROCEDURE get_movies()
BEGIN
	SELECT id, name, genre, duration_minutes, description
	FROM movie
	ORDER BY id;
END //

DROP PROCEDURE IF EXISTS check_movie //
CREATE PROCEDURE check_movie(IN id_movie INT)
BEGIN
	SELECT COUNT(*)
	FROM screening
	WHERE movie_id = id_movie;
END //

DROP PROCEDURE IF EXISTS check_movie_exists //
CREATE PROCEDURE check_movie_exists(IN id_movie INT)
BEGIN
	SELECT COUNT(*)
	FROM movie
	WHERE id = id_movie;
END //

DROP PROCEDURE IF EXISTS remove_cinema_hall //
CREATE PROCEDURE remove_cinema_hall(IN id_hall INT)
BEGIN
	DELETE FROM cinema_hall
	WHERE id = id_hall;
	COMMIT;
END //

DROP PROCEDURE IF EXISTS remove_movie //
CREATE PROCEDURE remove_movie(IN id_movie INT)
BEGIN
	DELETE FROM movie
	WHERE id = id_movie;
	COMMIT;
END //

DROP PROCEDURE IF EXISTS add_screening //
CREATE PROCEDURE add_screening(IN movie_id_screening INT, IN cinema_hall_id_screening INT, IN start_date_screening VARCHAR(255))
BEGIN
	INSERT INTO screening(movie_id, cinema_hall_id, start_date)
	VALUES (movie_id_screening, cinema_hall_id_screening, STR_TO_DATE(start_date_screening,'%Y-%m-%d %H:%i:%s'));
	COMMIT;
END //

DROP PROCEDURE IF EXISTS get_screenings //
CREATE PROCEDURE get_screenings(IN movie_id_screening INT)
BEGIN
	SELECT id, cinema_hall_id, concat(left(start_date, 10), ' ', right(start_date, 8))
	FROM screening
	WHERE movie_id = movie_id_screening
	ORDER BY id;
END //

DROP PROCEDURE IF EXISTS get_screenings_for_date //
CREATE PROCEDURE get_screenings_for_date(IN d VARCHAR(40))
BEGIN
	SELECT s.id, concat(left(s.start_date, 10), ' ', right(s.start_date, 8)), m.name, m.genre, m.duration_minutes, m.description
	FROM screening s, movie m
	WHERE STRCMP(left(s.start_date, 10), d) = 0 AND s.movie_id = m.id
	ORDER BY s.start_date;
END //

DROP PROCEDURE IF EXISTS check_screening_exists //
CREATE PROCEDURE check_screening_exists(IN id_screening INT)
BEGIN
	SELECT COUNT(*)
	FROM screening
	WHERE id = id_screening;
END //

DROP PROCEDURE IF EXISTS check_screening //
CREATE PROCEDURE check_screening(IN id_screening INT)
BEGIN
	SELECT COUNT(*)
	FROM reservation
	WHERE screening_id = id_screening;
END //

DROP PROCEDURE IF EXISTS check_reservation //
CREATE PROCEDURE check_reservation(IN id_reservation INT)
BEGIN
	SELECT COUNT(*)
	FROM reservation
	WHERE id = id_reservation;
END //

DROP PROCEDURE IF EXISTS check_reservation_purchased //
CREATE PROCEDURE check_reservation_purchased(IN id_reservation INT)
BEGIN
	SELECT purchased
	FROM reservation
	WHERE id = id_reservation;
END //

DROP PROCEDURE IF EXISTS remove_screening //
CREATE PROCEDURE remove_screening(IN id_screening INT)
BEGIN
	DELETE FROM screening
	WHERE id = id_screening;
	COMMIT;
END //

DROP PROCEDURE IF EXISTS remove_reservation //
CREATE PROCEDURE remove_reservation(IN id_reservation INT)
BEGIN
	DELETE FROM reservation
	WHERE id = id_reservation;
	COMMIT;
END //

DROP PROCEDURE IF EXISTS get_seats_for_screening //
CREATE PROCEDURE get_seats_for_screening(IN id_screening INT)
BEGIN
	SELECT s.row, s.number_seat, r.purchased
	FROM reservation r, seat s, reserved_seat rs
	WHERE r.screening_id = id_screening AND rs.reservation_id = r.id AND s.id = rs.seat_id
	ORDER BY s.row, s.number_seat;
END //

DROP PROCEDURE IF EXISTS get_number_of_seats_for_screening //
CREATE PROCEDURE get_number_of_seats_for_screening(IN id_screening INT)
BEGIN
	SELECT ch.number_of_rows, ch.number_of_seats_per_row
	FROM cinema_hall ch, screening s
	WHERE s.id = id_screening AND ch.id = s.cinema_hall_id;
END //

DROP PROCEDURE IF EXISTS get_reservations //
CREATE PROCEDURE get_reservations(IN id_screening INT)
BEGIN
	SELECT r.id, s.row, s.number_seat, r.purchased, r.credit_card_info
	FROM reservation r, seat s, reserved_seat rs
	WHERE r.screening_id = id_screening AND rs.reservation_id = r.id AND rs.seat_id = s.id
	ORDER BY s.row, s.number_seat;
END //

DROP PROCEDURE IF EXISTS add_reservation //
CREATE PROCEDURE add_reservation(IN id_screening INT)
BEGIN
	INSERT INTO reservation (screening_id, purchased, credit_card_info, time_of_reservation)
	VALUES (id_screening, 0, NULL, NOW());
	COMMIT;

	SELECT MAX(id)
	FROM reservation;
END //

DROP PROCEDURE IF EXISTS add_reserved_seat //
CREATE PROCEDURE add_reserved_seat(IN id_screening INT, IN id_reservation INT, IN row_number INT, IN seat_number INT)
BEGIN
	DECLARE id_seat INT;

	SELECT s.id INTO id_seat
	FROM seat s, screening sc
	WHERE sc.id = id_screening AND
		  sc.cinema_hall_id = s.cinema_hall_id AND
		  s.row = row_number AND
		  s.number_seat = seat_number;

	INSERT INTO reserved_seat (seat_id, reservation_id)
	VALUES (id_seat, id_reservation);
	COMMIT;
END //

DROP PROCEDURE IF EXISTS get_reservation_details //
CREATE PROCEDURE get_reservation_details(IN id_reservation INT)
BEGIN
	SELECT r.id, m.id, m.name, concat(left(s.start_date, 10), ' ', right(s.start_date, 8)), ch.name, r.purchased
	FROM reservation r, screening s, movie m, cinema_hall ch
	WHERE r.id = id_reservation AND
		  r.screening_id = s.id AND
		  s.movie_id = m.id AND
		  s.cinema_hall_id = ch.id;
END //

DROP PROCEDURE IF EXISTS get_seats_for_reservation //
CREATE PROCEDURE get_seats_for_reservation(IN id_reservation INT)
BEGIN
	SELECT s.row, s.number_seat
	FROM reserved_seat rs, seat s
	WHERE rs.reservation_id = id_reservation AND
		  rs.seat_id = s.id;
END //

DROP PROCEDURE IF EXISTS buy_reservation //
CREATE PROCEDURE buy_reservation(IN id_reservation INT, IN credit_card_info_reservation VARCHAR(255))
BEGIN
	UPDATE reservation
	SET purchased = 1, credit_card_info = credit_card_info_reservation
	WHERE id = id_reservation;
	COMMIT;
END //

DROP PROCEDURE IF EXISTS add_user //
CREATE PROCEDURE add_user(IN u_name VARCHAR(255), IN u_pass VARCHAR(255), IN u_role INT)
BEGIN
	INSERT INTO user(user_name, user_password, user_role)
	VALUES (u_name, u_pass, u_role);
	COMMIT;
END //

DROP PROCEDURE IF EXISTS check_user //
CREATE PROCEDURE check_user(IN u_name VARCHAR(255), IN u_pass VARCHAR(255))
BEGIN
	SELECT id, user_role
	FROM user
	WHERE user_name = u_name AND
	      user_password = u_pass;
END //

DROP PROCEDURE IF EXISTS get_users //
CREATE PROCEDURE get_users()
BEGIN
	SELECT *
	FROM user;
END //

DELIMITER ;

call add_cinema_hall('Londra', 10, 8);
call add_cinema_hall('Barcelona', 9, 10);

call add_movie('Miami Bici', 'Comedie', 98, 'Matei Dima si Codin Maticiuc interpreteaza rolurile a doi romani saraci, plecati in Miami ca sa atinga visul american si sa se imbogateasca');
call add_movie('Jumanji: Nivelul urmator', 'Actiune', 124, 'In Jumanji: Nivelul urmator jucatorii trebuie sa infrunte deserturi aride si munti inzapeziti pentru a scapa cu viata din cel mai periculos joc din lume');

call add_screening(1, 1, '2020-03-17 09:00:00');
call add_screening(2, 2, '2020-03-17 18:00:00');
call add_screening(1, 1, '2020-03-17 12:00:00');
call add_screening(1, 1, '2020-03-17 16:00:00');
call add_screening(1, 1, '2020-03-17 19:00:00');
call add_screening(1, 1, '2020-03-17 21:50:00');
call add_screening(2, 2, '2020-03-17 18:00:00');
call add_screening(2, 2, '2020-03-17 21:50:00');

call add_screening(1, 1, '2020-03-18 09:00:00');
call add_screening(2, 2, '2020-03-18 18:00:00');
call add_screening(1, 1, '2020-03-18 19:00:00');
call add_screening(1, 1, '2020-03-18 21:50:00');
call add_screening(2, 2, '2020-03-18 19:00:00');

call add_reservation(1);
call add_reservation(1);
call add_reservation(2);
INSERT INTO reservation (screening_id, purchased, credit_card_info, time_of_reservation)
VALUES (1, 0, NULL, DATE_SUB(DATE(NOW()), INTERVAL 2 DAY));
COMMIT;
INSERT INTO reservation (screening_id, purchased, credit_card_info, time_of_reservation)
VALUES (1, 0, NULL, DATE_SUB(DATE(NOW()), INTERVAL 2 DAY));
COMMIT;
INSERT INTO reservation (screening_id, purchased, credit_card_info, time_of_reservation)
VALUES (1, 0, NULL, DATE_SUB(DATE(NOW()), INTERVAL 1 DAY));
COMMIT;


call add_reserved_seat(1, 1, 2, 1);
call add_reserved_seat(1, 1, 2, 2);
call add_reserved_seat(1, 1, 2, 3);
call add_reserved_seat(1, 2, 3, 3);
call add_reserved_seat(1, 2, 3, 4);
call add_reserved_seat(2, 3, 2, 4);
call add_reserved_seat(2, 3, 2, 5);

call buy_reservation(1, "INFO");

call add_user('admin', 'adminpass', 0);
call add_user('client', 'clientpass', 1);
