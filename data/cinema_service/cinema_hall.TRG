TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER add_seats_new_cinema_hall\n    AFTER INSERT ON cinema_hall\n    FOR EACH ROW \nBEGIN\n	DECLARE r INT;\n	DECLARE s INT;\n	SET r = new.number_of_rows;\n	SET s = new.number_of_seats_per_row;\n\n	REPEAT\n		SET s = new.number_of_seats_per_row;\n		REPEAT\n    		INSERT INTO seat (cinema_hall_id, row, number_seat)\n			VALUES (new.id, r, s);\n			SET s = s - 1;\n			UNTIL s <= 0\n		END REPEAT;\n		SET r = r - 1;\n		UNTIL r <= 0\n	END REPEAT;\nEND' 'CREATE DEFINER=`root`@`localhost` TRIGGER remove_seats_remove_cinema_hall\n    BEFORE DELETE ON cinema_hall\n    FOR EACH ROW \nBEGIN\n	DELETE FROM seat\n	WHERE cinema_hall_id = old.id;\nEND'
sql_modes=1436549152 1436549152
definers='root@localhost' 'root@localhost'
client_cs_names='latin1' 'latin1'
connection_cl_names='latin1_swedish_ci' 'latin1_swedish_ci'
db_cl_names='latin1_swedish_ci' 'latin1_swedish_ci'
created=158464636777 158464636790
