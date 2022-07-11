# -*- coding: utf-8 -*-
import json

from helpers import load_config, create_logger
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Union, Optional
from users import Users


class User(BaseModel):
    name: str
    role: str
    password: str

# Load config file
conf = load_config()

# Create logger
logger = create_logger(conf)

api = FastAPI(
    title=conf['api.name'],
    description=conf['api.description'],
    version=conf['api.version'],
    openapi_tags=[
        {'name': 'Home', 'description': ''},
        {'name': 'User', 'description': 'Check user'}
    ]
)

security = HTTPBasic()

responses_user = {
    401: {"description": "Incorrect username or password"},
    418: {"description": "Username not admin"},
    422: {"description": "User unknown"}
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

@api.get('/auth_test', name='Verify user authentication', tags=['User'])
async def authentication_test(username: str = Depends(check_authent_credentials)):
    if username:
        return {'detail': 'Authentication OK'}