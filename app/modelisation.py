# -*- coding: utf-8 -*-
import numpy as np
import pickle

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


# Evaluation model
def evaluation(logger, model, X_train, y_train, X_test, y_test):    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    logger.info("Confusion matrix :\n", confusion_matrix(y_test, y_pred))
    logger.info("Classif. report :\n", classification_report(y_test, y_pred))


def best_params(logger, model, X_train, y_train):
    params = {'selectkbest__k': range(1, 11)}
    grid = GridSearchCV(model, params, scoring='f1', cv=5)
    grid.fit(X_train, y_train)
    logger.info("Model best params : %s" %grid.best_params_)


# Choose the best model
def best_classifier(logger, strategy, X_train, y_train, X_test, y_test):
    logistic_regression = make_pipeline(
        SimpleImputer(missing_values=np.nan, strategy=strategy),
        SelectKBest(f_classif, k=10),
        LogisticRegression(random_state=0)
    )
    
    decision_tree = make_pipeline(
        SimpleImputer(missing_values=np.nan, strategy=strategy),
        SelectKBest(f_classif, k=10),
        DecisionTreeClassifier(random_state=0)
    )
    
    kneighbors = make_pipeline(
        SimpleImputer(missing_values=np.nan, strategy=strategy),
        SelectKBest(f_classif, k=10),
        KNeighborsClassifier(n_neighbors=5)
    )

    models = {
        'LogisticRegression': logistic_regression,
        'DecisionTree' : decision_tree,
        'KNeighbors': kneighbors
    }

    for name, model in models.items():
        logger.info("Model : %s" %name)
        
        # Model evaluation
        evaluation(logger, model, X_train, y_train, X_test, y_test)

        # Optimization model parameters
        best_params(logger, model, X_train, y_train)


# Serialize on disk ml model
def serialize_ml_model(conf, model_name, X_train, y_train):
    if model_name == 'logistic_regression':
        ml_model = make_pipeline(
            SimpleImputer(missing_values=np.nan, strategy='mean'),
            SelectKBest(f_classif, k=10),
            LogisticRegression(random_state=0)
        )
        pkl_file = conf['model.path'] + '/' + conf['model.file.lr']
    elif model_name == 'decision_tree':
        ml_model = make_pipeline(
            SimpleImputer(missing_values=np.nan, strategy='mean'),
            SelectKBest(f_classif, k=8),
            DecisionTreeClassifier(random_state=0)
        )
        pkl_file = conf['model.path'] + '/' + conf['model.file.tree']
    elif model_name == 'kneighbors':
        ml_model = make_pipeline(
            SimpleImputer(missing_values=np.nan, strategy='mean'),
            SelectKBest(f_classif, k=10),
            KNeighborsClassifier(n_neighbors=5)
        )
        pkl_file = conf['model.path'] + '/' + conf['model.file.kn']

    # Fit model
    ml_model.fit(X_train, y_train)

    # Serialize model
    pkl_ml_model = open(pkl_file, 'wb')
    pickle.dump(ml_model, pkl_ml_model)


# Deserialize model 
def load_model(dump_model_file):
    ml_model_pkl = open(dump_model_file, 'rb')
    ml_model = pickle.load(ml_model_pkl)
    return ml_model


# Get performance model
def perf_model(dump_ml_model, X_train, y_train, X_test, y_test):
    ml_model = dump_ml_model
    ml_model.fit(X_train, y_train)
    y_pred = ml_model.predict(X_test)
    ml_model_perf = classification_report(y_test, y_pred, output_dict=True)
    return ml_model_perf