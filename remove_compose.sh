docker-compose down

ADMIN_INTERFACE=$(docker container ls -a | grep "cinema-proiect_admin-interface" | sed 's/  */ /g' | cut -d' ' -f1)
ADMIN=$(docker container ls -a | grep "cinema-proiect_admin" | sed 's/  */ /g' | cut -d' ' -f1)
DB=$(docker container ls -a | grep "mysql" | sed 's/  */ /g' | cut -d' ' -f1)
CLIENT=$(docker container ls -a | grep "client" | sed 's/  */ /g' | cut -d' ' -f1)
SERVER=$(docker container ls -a | grep "server" | sed 's/  */ /g' | cut -d' ' -f1)
GRAFANA=$(docker container ls -a | grep "grafana" | sed 's/  */ /g' | cut -d' ' -f1)
AUTH=$(docker container ls -a | grep "auth" | sed 's/  */ /g' | cut -d' ' -f1)


docker container rm $ADMIN_INTERFACE
docker container rm $ADMIN
docker container rm $DB
docker container rm $CLIENT
docker container rm $SERVER
docker container rm $GRAFANA
docker container rm $AUTH

ADMIN_INTERFACE=$(docker image ls -a | grep "cinema-proiect_admin-interface" | sed 's/  */ /g' | cut -d' ' -f3)
ADMIN=$(docker image ls -a | grep "cinema-proiect_admin" | sed 's/  */ /g' | cut -d' ' -f3)
DB=$(docker image ls -a | grep "mysql" | sed 's/  */ /g' | cut -d' ' -f3)
CLIENT=$(docker image ls -a | grep "client" | sed 's/  */ /g' | cut -d' ' -f3)
SERVER=$(docker image ls -a | grep "server" | sed 's/  */ /g' | cut -d' ' -f3)
AUTH=$(docker image ls -a | grep "auth" | sed 's/  */ /g' | cut -d' ' -f3)

docker image rm $ADMIN_INTERFACE
docker image rm $ADMIN
docker image rm $DB
docker image rm $CLIENT
docker image rm $SERVER
docker image rm $AUTH