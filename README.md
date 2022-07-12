# DataScientest - Cursus DE - Projet Strokes (ML + Indus)

## Installation

__A noter__ : Tests effectués avec Docker sous Windows

### Optionnel : Construction des image mysql avec la BDD Strokes (image déjà pushées sous github)
```sh
## DB
# Construction image mysql avec la BDD strokes
docker image build --force-rm --tag classerredev/mysql-db-strokes:latest --file dockerfile-db .
# Push image sur mon github
docker image push classerredev/mysql-db-strokes:latest

## API
# Construction image API strokes
docker image build --force-rm --tag classerredev/api-strokes:latest --file dockerfile-api .
# Push image sur mon github
docker image push classerredev/api-strokes:latest

## API test
# Construction image API strokes test
docker image build --force-rm --tag classerredev/api-test-strokes:latest --file dockerfile-api-test .

# Push image sur mon github
docker image push classerredev/api-test-strokes:latest
```


### Requis : Lancement du docker-compose
```sh
# Modifier le docker-compose pour concernant 
# le répertoire local du volume pour strokes-api-test
docker-compose up -d --force-recreate

# Vérifier logs
docker logs strokes-mysql-db
docker logs strokes-api-server
docker logs strokes-api-test
```


### Optionnel : Pour tester/explorer la BDD
```sh
# Exécuter container mysql pour test
docker exec -it strokes-mysql-db bash

# Lancer le client mysql
mysql -uroot -pdata

# Lancer une requête avec le client mysql
SELECT user_id, user_name, user_role, 
CONVERT(AES_DECRYPT(user_password, 'strokes') using utf8) AS user_password
FROM strokes.users;
exit
```


### Optionnel : Pour tester l'API
```sh
# Lancer container api-test
docker run -it --rm \
-e API_HOST=strokes-api-server \
-e API_PORT=8000 \
--network strokes \
classerredev/api-test-strokes:latest bash

# Tester les endpoint
curl -X GET -i 'http://strokes-api-server:8000/status'

curl -X GET -i 'http://strokes-api-server:8000/auth_test' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET -i 'http://strokes-api-server:8000/model/perf?model_name=decision_tree' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET -i 'http://strokes-api-server:8000/model/perf?model_name=logistic_regression' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET -i 'http://strokes-api-server:8000/model/perf?model_name=kneighbors' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

exit
```

kubectl get pod -o template --template={{.status.podIP}}
https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/
https://stackoverflow.com/questions/69686202/kubernetes-ingress-objects-return-no-response-on-windows-10-minikube
https://k3d.io/v5.0.0/usage/exposing_services/