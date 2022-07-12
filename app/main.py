# -*- coding: utf-8 -*-
import pandas as pd
import sys

from sklearn.tree import DecisionTreeClassifier

from helpers import load_config, create_logger
from pre_processing import encoding, scaling, pre_processing
from modelisation import best_classifier, serialize_ml_model, load_model, perf_model


def display_conf(logger):
    logger.debug('api.name : %s' % conf['api.name'])
    logger.debug('api.description : %s' % conf['api.description'])
    logger.debug('api.version : %s' % conf['api.version'])    
    logger.debug('data.path : %s' % conf['data.path'])
    logger.debug('data.file : %s' % conf['data.file'])
    logger.debug('data.file.separator : %s' % conf['data.file.separator'])
    logger.debug('data.file.header : %s' % conf['data.file.header'])        
    logger.debug('log.path : %s' % conf['log.path'])
    logger.debug('log.level : %s' % conf['log.level'])
    logger.debug('log.file : %s' % conf['log.file'])
    logger.debug('model.path : %s' % conf['model.path'])
    logger.debug('model.file.lr : %s' % conf['model.file.lr'])
    logger.debug('model.file.tree : %s' % conf['model.file.tree'])
    logger.debug('model.file.kn : %s' % conf['model.file.kn'])


if __name__ == "__main__":
    conf = load_config()    
    logger = create_logger(conf)
    # display_conf(logger)
            
    X_train, X_test, y_train, y_test = pre_processing(conf, sampling=False)    
    # logger.debug("X_train : %s / y_train %s" %(X_train.shape, y_train.shape))
    # logger.debug("X_test : %s / y_test %s" %(X_test.shape, y_test.shape))
    # logger.debug("y_train :\n%s" %y_train.value_counts())
    # logger.debug("y_test :\n%s" %y_test.value_counts())

    function = sys.argv[1]
    if function == 'best':
        best_classifier(logger, 'mean', X_train, y_train, X_test, y_test)
    
    elif function == 'save':
        model_name = sys.argv[2]
        serialize_ml_model(conf, model_name, X_train, y_train)
    
    elif function == 'predict':
        model_name = sys.argv[2]
        if model_name == 'logistic_regression':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.lr']
        elif model_name == 'decision_tree':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.tree']
        elif model_name == 'kneighbors':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.kn']
        model = load_model(dump_ml_model_file)

        ALL_FEATURES = [
            'age', 'avg_glucose_level', 'bmi', 'gender',  'ever_married',
            'work_type', 'residence_type', 'smoking_status', 'hypertension',
            'heart_disease'
        ]

        QUANTITATIVE_FEATURES = [
            'age', 'avg_glucose_level', 'bmi'
        ]

        QUALITATIVE_FEATURES = [
            'gender', 'ever_married', 'work_type', 'residence_type',
            'smoking_status', 'hypertension', 'heart_disease'
        ]

        data = {
            'age': [55, 21],
            'gender': ['Male', 'Female'],
            'work_type': ['Private', 'Private'],
            'residence_type': ['Urban', 'Rural'],
            'ever_married': ['Yes', 'No'],
            'smoking_status': ['formerly smoked', 'never smoked'],
            'hypertension': [0, 0],
            'heart_disease': [0, 0],
            'bmi': [30, 21.8],
            'avg_glucose_level': [250, 55.12]
        }

        X = pd.DataFrame(data)    
        X_quantitative = X.loc[:, QUANTITATIVE_FEATURES]
        X_qualitative = encoding(X, QUALITATIVE_FEATURES)                
        X = pd.concat([X_quantitative, X_qualitative], axis=1)                
        
        y_pred = model.predict(X)                        
        X = X.assign(stroke=y_pred.tolist())
        print(X.head())

    elif function == 'perf':
        ml_model_name = sys.argv[2]
        if ml_model_name == 'logistic_regression':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.lr']
        elif ml_model_name == 'decision_tree':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.tree']
        elif ml_model_name == 'kneighbors':
            dump_ml_model_file = conf['model.path'] + '/' + conf['model.file.kn']
        ml_model = load_model(dump_ml_model_file)

        ml_model_perf = perf_model(ml_model, X_train, y_train, X_test, y_test)
        print(ml_model_perf)