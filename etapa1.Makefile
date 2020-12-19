run:
	sudo docker container run -it etapa1 python admin-interface.py http://google.com

build:
	sudo docker build --rm -t etapa1 admin-interface
