# -*- coding: utf-8 -*-
import json
import logging
import os

from logging import FileHandler, Formatter, StreamHandler


def load_config():
    package_dir = os.path.dirname(__file__)
    file_name = (os.path.join(package_dir, 'conf/cfg.json'))
    with open(file_name, 'r') as f:
        conf = json.load(f)
    return conf

def create_logger(conf):
    app_name = conf['api.name']
    log_level = conf['log.level']
    log_file = conf['log.path'] + '/' + conf['log.file']

    # Create logger
    logger = logging.getLogger(app_name)

    # Define log level
    if log_level == 'ERROR':
        logger.setLevel(logging.ERROR)        
    elif log_level == 'WARING':
        logger.setLevel(logging.WARN)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)

    # Define log format
    formatter: Formatter = Formatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s")

    # Console output
    console_handler: StreamHandler = StreamHandler()    
    console_handler.setFormatter(formatter)

    # File output
    file_handler: FileHandler = FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger    