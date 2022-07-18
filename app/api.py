# -*- coding: utf-8 -*-
import json
import os

from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Union, Optional

from helpers import load_config, create_logger
from users import Users
from pre_processing import pre_processing
from modelisation import load_model, perf_model


class User(BaseModel):
    name: str
    role: str
    password: str

# Load config file
conf = load_config()

# Create logger
logger = create_logger(conf)

# To manage network on Kube or docker-compose
if os.getenv(conf['env.kube.mysql.host']) is None:
    mysql_host = str(os.getenv('MYSQL_HOST'))
else:
    mysql_host = str(os.getenv(conf['env.kube.mysql.host']))

if os.getenv(conf['env.kube.mysql.port']) is None:
    mysql_port = str(os.getenv('MYSQL_PORT'))
else:
    mysql_port = str(os.getenv(conf['env.kube.mysql.port']))

mysql_url = mysql_host + ':' + mysql_port
mysql_dbname = os.getenv('MYSQL_DATABASE')
mysql_user = os.getenv('MYSQL_ROOT_USER')
mysql_password = os.getenv('MYSQL_ROOT_PASSWORD')
mysql_encrypt_key = os.getenv('MYSQL_ENCRYPT_KEY')

#  Create mysql url connection
mysql_connection_url = 'mysql+mysqlconnector://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=mysql_dbname
)
print('mysql_connection_url : ', mysql_connection_url)

try:
    mysql_engine = create_engine(mysql_connection_url)        

except SQLAlchemyError as err:
    logger.error(err)


# Init users for authent
users = Users(conf, logger, mysql_engine, mysql_encrypt_key)

# Split, cleaning, encoding
X_train, X_test, y_train, y_test = pre_processing(conf, sampling=False)

api = FastAPI(
    title=conf['api.name'],
    description=conf['api.description'],
    version=conf['api.version'],
    openapi_tags=[
        {'name': 'Home', 'description': ''},
        {'name': 'User', 'description': 'Manage user'},
        {'name': 'User', 'description': 'Machine learning concerning strokes'}
    ]
)

security = HTTPBasic()

http_responses = {
    401: {"description": "Incorrect username or password"},
    418: {"description": "Model not found"}
}

def check_authent_credentials(credentials: HTTPBasicCredentials=Depends(security)):
    result = users.verify_username_password(credentials.username, credentials.password)
    if result < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password')
    else:
        return credentials.username


@api.get('/status', name='Status', tags=['Home'])
async def welcome():
    """Check API Status
    """
    return {'detail': 'API Status OK'}


@api.get(
    '/auth_test',
    name='Verify user authentication',
    tags=['User'],
    responses=http_responses
)
async def auth_test(username: str = Depends(check_authent_credentials)):
    if username:
        return {'detail': 'Authentication OK'}
    else:
        raise HTTPException(
                status_code=401,
                detail='Incorrect username or password')


@api.get(
    '/model/perf',
    name='Get Decision Tree model performance',
    tags=['Model'],
    responses=http_responses
)
async def model_perf(model_name: str, username: str = Depends(check_authent_credentials)):
    if username:
        if model_name == 'logistic_regression':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.lr']
        elif model_name == 'decision_tree':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.tree']
        elif model_name == 'kneighbors':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.kn']
        else:
            raise HTTPException(
                status_code=418,
                detail='User added')
        ml_model = load_model(dump_ml_model_file)
        ml_model_perf = perf_model(ml_model, X_train, y_train, X_test, y_test)
        return json.dumps(ml_model_perf)
    else:
        raise HTTPException(
                status_code=401,
                detail='Incorrect username or password')