# DataScientest - Cursus DE - Projet Strokes (ML + Indus)

## Installation

### Optionnel : Construction des image mysql avec la BDD Strokes (image déjà pushées sous github)
```sh
## DB
# Construction image mysql avec la BDD strokes
docker image build --force-rm --tag classerredev/mysql-db-strokes:latest --file dockerfile-db .
# Push image sur mon github
docker image push classerredev/mysql-db-strokes:latest

# API
# Construction image API strokes
docker image build --force-rm --tag classerredev/api-strokes:latest --file dockerfile-api .
# Push image sur mon github
docker image push classerredev/api-strokes:latest
```

### Optionnel : Pour tester/explorer la BDD
```sh
# Lancement container mysql pour test
docker run --rm -d \
-e MYSQL_ROOT_PASSWORD=data \
-e MYSQL_DATABASE=strokes \
--name strokes-db classerredev/mysql-db-strokes:latest

# En mode CLI dans le container
docker exec -it strokes-db bash
mysql -uroot -pdata
SELECT user_id, user_name, user_role, CONVERT(AES_DECRYPT(user_password, 'strokes') using utf8) AS user_password FROM strokes.users;

# Arrêt container
docker container stop strokes-db

# Si problème pour consulter les logs
docker logs strokes-db
```

### Optionnel : Pour tester l'API
```sh
docker run --rm -d \
-e MYSQL_HOST=strokes-db \
-e MYSQL_PORT=3306 \
-e MYSQL_DATABASE=strokes \
-e MYSQL_ROOT_USER=root \
-e MYSQL_ROOT_PASSWORD=data \
-e MYSQL_ENCRYPT_KEY=strokes \
--name strokes-api classerredev/api-strokes:latest

# En mode CLI dans le container
docker exec -it strokes-api bash

# Arrêt container
docker container stop strokes-api

# Si problème pour consulter les logs
docker logs strokes-api
```

```sh
docker-compose up -d --force-recreate

# Vérifier log db
docker logs strokes-db

# Vérifier log API
docker logs strokes-api

# Pour tester les APIs
curl -X GET -i 'http://localhost:8000/status'

curl -X GET -i 'http://localhost:8000/auth_test' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='
```
