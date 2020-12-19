sudo docker-compose down

ADMIN_INTERFACE=$(sudo docker container ls -a | grep "cinema-proiect_admin-interface" | sed 's/  */ /g' | cut -d' ' -f1)
ADMIN=$(sudo docker container ls -a | grep "cinema-proiect_admin" | sed 's/  */ /g' | cut -d' ' -f1)
DB=$(sudo docker container ls -a | grep "mysql" | sed 's/  */ /g' | cut -d' ' -f1)
CLIENT=$(sudo docker container ls -a | grep "client" | sed 's/  */ /g' | cut -d' ' -f1)
SERVER=$(sudo docker container ls -a | grep "server" | sed 's/  */ /g' | cut -d' ' -f1)
GRAFANA=$(sudo docker container ls -a | grep "grafana" | sed 's/  */ /g' | cut -d' ' -f1)


sudo docker container rm $ADMIN_INTERFACE
sudo docker container rm $ADMIN
sudo docker container rm $DB
sudo docker container rm $CLIENT
sudo docker container rm $SERVER
sudo docker container rm $GRAFANA

ADMIN_INTERFACE=$(sudo docker image ls -a | grep "cinema-proiect_admin-interface" | sed 's/  */ /g' | cut -d' ' -f3)
ADMIN=$(sudo docker image ls -a | grep "cinema-proiect_admin" | sed 's/  */ /g' | cut -d' ' -f3)
DB=$(sudo docker image ls -a | grep "mysql" | sed 's/  */ /g' | cut -d' ' -f3)
CLIENT=$(sudo docker image ls -a | grep "client" | sed 's/  */ /g' | cut -d' ' -f3)
SERVER=$(sudo docker image ls -a | grep "server" | sed 's/  */ /g' | cut -d' ' -f3)


sudo docker image rm $ADMIN_INTERFACE
sudo docker image rm $ADMIN
# sudo docker image rm $DB
sudo docker image rm $CLIENT
sudo docker image rm $SERVER