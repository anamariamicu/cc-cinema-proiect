TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER remove_reserved_seats\n    BEFORE DELETE ON reservation\n    FOR EACH ROW \nBEGIN\n	DELETE FROM reserved_seat\n	WHERE reservation_id = old.id;\nEND'
sql_modes=1436549152
definers='root@localhost'
client_cs_names='latin1'
connection_cl_names='latin1_swedish_ci'
db_cl_names='latin1_swedish_ci'
created=158464636784
