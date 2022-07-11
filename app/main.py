# -*- coding: utf-8 -*-
import pandas as pd
import sys

from sklearn.tree import DecisionTreeClassifier

from helpers import load_config, create_logger
from pre_processing import encoding, scaling, pre_processing
from modelisation import best_classifier, dump_decision_tree_model, load_decision_tree_model


def display_conf(logger):
    logger.debug('app.name : %s' % conf['app.name'])
    logger.debug('app.description : %s' % conf['app.description'])
    logger.debug('app.version : %s' % conf['app.version'])    
    logger.debug('data.path : %s' % conf['data.path'])
    logger.debug('data.db : %s' % conf['data.db'])
    logger.debug('data.file : %s' % conf['data.file'])
    logger.debug('data.file.separator : %s' % conf['data.file.separator'])
    logger.debug('data.file.header : %s' % conf['data.file.header'])        
    logger.debug('log.path : %s' % conf['log.path'])
    logger.debug('log.level : %s' % conf['log.level'])
    logger.debug('log.file : %s' % conf['log.file'])


if __name__ == "__main__":
    ALL_FEATURES = ['age', 'avg_glucose_level', 'bmi', 'gender', 
                    'ever_married', 'work_type', 'residence_type', 
                    'smoking_status', 'hypertension', 'heart_disease']

    QUANTITATIVE_FEATURES = ['age', 'avg_glucose_level', 'bmi']

    QUALITATIVE_FEATURES = ['gender', 'ever_married', 'work_type', 
                            'residence_type', 'smoking_status', 'hypertension',
                            'heart_disease']                    

    conf = load_config()    
    logger = create_logger(conf)
    display_conf(logger)
            
    X_train, X_test, y_train, y_test = pre_processing(conf, sampling=False)    
    logger.debug("X_train : %s / y_train %s" %(X_train.shape, y_train.shape))
    logger.debug("X_test : %s / y_test %s" %(X_test.shape, y_test.shape))
    logger.debug("y_train :\n%s" %y_train.value_counts())
    logger.debug("y_test :\n%s" %y_test.value_counts())

    function = sys.argv[1]
    if function == 'best_model':
        best_classifier(logger, 'mean', X_train, y_train, X_test, y_test)
    
    elif function == 'save_model':
        dump_decision_tree_model(conf, X_train, y_train)
    
    elif function == 'predict':
        model = load_decision_tree_model(conf)
        
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