DataScientest - Cursus DE
========
Projet Strokes (ML + Indus)
--------
- - - -

<br>

# 1. Notes techniques

## Environnement de développement/test
* Ubuntu avec WSL2 (sous Windows 11)
* Docker 20.10.17
* Minikube 1.26.0
  *  L'installation et la configuration de minikube a été effectué en suivant la procédure :
     *  https://blog.ineat-group.com/2020/06/utiliser-kubernetes-en-local-avec-minikube-sous-windows-10/
* Python 3.8.10 

<br>

## Choix techniques
* Pour le développement de l'api, utilisation de la librairie fastapi :
  * 3 endpoints ont été développés :
    * /status : Vérifier si le statut de l'API
    * /auth_test : Vérifier l'authentification de l'API
    * /model/perf : Récupérér les performances d'un modèle (Régression linéaire, Decision Tree, KNeighbors)
* Les utilisateurs sont stockées dans une table users de la base de données mysql "Strokes"
  * Les mots de passe sont encryptés avec une fonction mysql AES_ENCRYPT avec une clé ayant la valeur "strokes"
  * Cette clé est stocké dans une variable d'environnement du container

<br>

* Pour la partie docker-compose, 3 containers distincts :
  * 1 container pour mysql
  * 1 container pour l'api server
  * 1 container pour les tests de l'api

<br>

* Pour la partie Kubernetes :
  * 4 pods :
    * 1 pod pour mysql
    * 3 pods pour l'api server
  * Le hostname et le port de la BDD sont stockés dans des variables d'environnement dans les pods de l'api
    * Kubernetes créé ces variables d'environnement dans les pods à partir de la définition des services
  * L'ingress a été paramétré sur le host "strokes.kub" et a été rajouté dans le /etc/hosts avec l'IP de l'ingress
    
<br>

# 2. Installation

<br>

## Etape 1 (optionnelle) : Construction images docker mysql et API
```sh
## Pour la partie BDD avec MySQL
# Construction et push image mysql avec la BDD strokes
docker image build --force-rm --tag classerredev/mysql-db-strokes:latest --file dockerfile-db .
docker image push classerredev/mysql-db-strokes:latest

## Pour la partie API
# Construction image et push API strokes
docker image build --force-rm --tag classerredev/api-strokes:latest --file dockerfile-api .
docker image push classerredev/api-strokes:latest

## Pour la partie API test
# Construction et push image API strokes test
docker image build --force-rm --tag classerredev/api-test-strokes:latest --file dockerfile-api-test .
docker image push classerredev/api-test-strokes:latest
```

<br>

__A noter__ :<br>
Cette étape est optionnelle car ces images ont été publiées sur Dockerhub.<br>
En lieu et place de l'étape 1, il faut effectuer un docker pull
```sh
docker image pull classerredev/mysql-db-strokes:latest
docker image pull classerredev/api-strokes:latest
docker image pull classerredev/api-test-strokes:latest
```

<br>

## Etape 2 : Partie docker-compose pour les tests de l'API
```sh
# Modifier le docker-compose pour concernant 
# le répertoire local du volume pour strokes-api-test
docker-compose up -d --force-recreate

# Vérifier logs des containers
docker logs strokes-mysql-db
docker logs strokes-api-server
docker logs strokes-api-test
```

<br>

## Etape 2.1 (optionnelle) : Pour tester/explorer la BDD
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

<br>

## Etape 2.2 (optionnelle) : Pour tester l'API
```sh
# Lancer container api-test (adapter le mapping sur les volumes)
docker run -it --rm \
-e API_HOST=strokes-api-server \
-e API_PORT=8000 \
-e API_LOG=1 \
-e API_LOG_PATH=logs \
-v //c/Users/lasse/01_DEV/99_Logs:/app/test/logs \
--network strokes \
--name strokes-api-client \
classerredev/api-test-strokes:latest bash

# Tester les endpoint
curl -X GET 'http://strokes-api-server:8000/status'

curl -X GET 'http://strokes-api-server:8000/auth_test' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET 'http://strokes-api-server:8000/model/perf?model_name=decision_tree' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET 'http://strokes-api-server:8000/model/perf?model_name=logistic_regression' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET 'http://strokes-api-server:8000/model/perf?model_name=kneighbors' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

# Tester le script
# Côté WSL : les logs sont dans le répertoire \\wsl.localhost\Ubuntu\c\Users\lasse\99_TMP\log
./launch_test.sh

exit
```

<br>

## Etape 3 : Déploiement Kubernetes
```sh
# Création PV et PVC (pour mysql)
kubectl apply -f strokes-pv.yml
kubectl apply -f strokes-pvc.yml

# Création secrets (pour mysql)
kubectl apply -f strokes-secret.yml

# Création services
kubectl apply -f strokes-svc-db.yml
kubectl apply -f strokes-svc-api.yml

# Création ingress
kubectl apply -f strokes-ingress.yml

# Création deployments
kubectl apply -f strokes-deploy-db.yml
kubectl apply -f strokes-deploy-api.yml
```

<br>

## Etape 4 : Tests API
```sh
# Récupérer l'adresse IP de l'ingress
# Sans éditer le fichier /etc/hosts
curl -X GET http://192.168.49.2/status \
-H "Host:strokes.kub" \

curl -X GET http://192.168.49.2/auth_test \
-H "Host:strokes.kub" \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET http://192.168.49.2/model/perf?model_name=decision_tree \
-H "Host:strokes.kub" \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET http://192.168.49.2/auth_test \
-H "Host:strokes.kub" \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

# - Récupérer l'adresse IP de l'ingress
# - Editer le fichier /etc/hosts afin de rajouter
#     [IP Ingress] strokes.kub
curl -X GET -i http://strokes.kub/status

curl -X GET -i http://strokes.kub/auth_test \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET -i http://strokes.kub/model/perf?model_name=decision_tree \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET -i http://strokes.kub/model/perf?model_name=logistic_regression \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='

curl -X GET -i http://strokes.kub/model/perf?model_name=kneighbors \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic YWRtaW46NGRtMU4='
```