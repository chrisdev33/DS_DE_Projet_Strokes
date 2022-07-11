# DataScientest - Cursus DE - Projet Strokes (ML + Indus)

Optionnel : Construction de l'image mysql avec la BDD Strokes
(Présente sous github)
```sh
docker image build --force-rm --tag classerredev/mysql-db-strokes:latest --file dockerfile-db .
docker image build --force-rm --tag classerredev/api-strokes:latest --file dockerfile-api .
```

Optionnel : Pour tester/explorer la BDD
```sh
docker run --rm -d -p 3306:3306 --name strokes-db classerredev/mysql-db-strokes:latest
docker exec -it strokes-db bash

mysql -uroot -pdata
SELECT user_id, user_name, user_role, CONVERT(AES_DECRYPT(user_password, 'strokes') using utf8) AS user_password FROM strokes.users;

docker container stop strokes-db
```

Optionnel : Si problème lors du lancement du container
```sh
docker logs strokes-db
docker container rm -f strokes-db
docker image rm classerredev/mysql-db-strokes:0.1
```

```sh
docker-compose up -d --force-recreate
```

Pour tester les APIs
```sh
curl -X GET -i 'http://localhost:8000/status'

curl -X GET -i 'http://localhost:8000/auth_test' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='
```
