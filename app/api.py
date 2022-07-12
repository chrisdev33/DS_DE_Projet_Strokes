# -*- coding: utf-8 -*-
import json

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
    users = Users(conf, logger)
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


