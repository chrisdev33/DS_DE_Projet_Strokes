# DS_DE_Projet_Strokes



```sh
docker-compose up -d --force-recreate
```


curl -X GET -i 'http://localhost:8000/status'

curl -X GET -i 'http://localhost:8000/auth_test' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='


Optionnel : Construction de l'image mysql avec la BDD Strokes
(Présente sous github)
```sh
docker image build --force-rm --tag classerredev/mysql-db-strokes:latest --file dockerfile-db .
docker image build --force-rm --tag classerredev/api-strokes:latest --file dockerfile-api .
```

Optionnel : Pour tester la connexion à la BDD
```sh
docker run -it -p 3306:3306 --name  mysql-db-strokes classerredev/mysql-db-strokes:latest bash
docker exec -it mysql-db-strokes bash

docker run --rm -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=data --name mysql-db-strokes classerredev/mysql-db-strokes:latest

-e MYSQL_ROOT_PASSWORD=my-secret-pw


docker run -it -p 8000:8000 --name strokes-api-test classerredev/api-strokes:latest bash

mysql -uroot -pdatascientest1234
SELECT user_id, user_name, user_role, CONVERT(AES_DECRYPT(user_password, 'strokes') using utf8) AS user_password FROM strokes.users;
```

Optionnel : Si problème lors du lancement du container
```sh
docker logs mysql-db-strokes
docker container rm -f mysql-db-strokes
docker image rm classerredev/mysql-db-strokes:0.1
```

