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

    logger.info("Confusion matrix :\n%s" %confusion_matrix(y_test, y_pred))
    logger.info("Classification report :\n%s" 
                %classification_report(y_test, y_pred))

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
        LogisticRegression(random_state=0))
    
    decision_tree = make_pipeline(
        SimpleImputer(missing_values=np.nan, strategy=strategy),
        SelectKBest(f_classif, k=10),
        DecisionTreeClassifier(random_state=0))
    
    k_neighbors = make_pipeline(
        SimpleImputer(missing_values=np.nan, strategy=strategy),
        SelectKBest(f_classif, k=10),
        KNeighborsClassifier(n_neighbors=5))

    models = {'LogisticRegression': logistic_regression,
              'DecisionTree' : decision_tree,
              'KNeighbors': k_neighbors}

    for name, model in models.items():
        logger.info("Model : %s" %name)
        
        # Model evaluation
        evaluation(logger, model, X_train, y_train, X_test, y_test)

        # Optimization model parameters
        best_params(logger, model, X_train, y_train)

# Serialize on disk decision tree model
def dump_decision_tree_model(conf, X_train, y_train):
    decision_tree_model = make_pipeline(
        SimpleImputer(missing_values=np.nan, strategy='mean'),
        SelectKBest(f_classif, k=8),
        DecisionTreeClassifier(random_state=0))

    decision_tree_model.fit(X_train, y_train)
    
    # Open the file to save as pkl file
    decision_tree_pkl_filename = conf['model.path'] + '/decision_tree_classifier.pkl'
    decision_tree_model_pkl = open(decision_tree_pkl_filename, 'wb')
    pickle.dump(decision_tree_model, decision_tree_model_pkl)
    
    # Close the pickle instances
    decision_tree_model_pkl.close()

# Load serialized decision tree model
def load_decision_tree_model(conf):
    decision_tree_pkl_filename = conf['model.path'] + '/decision_tree_classifier.pkl'
    decision_tree_model_pkl = open(decision_tree_pkl_filename, 'rb')
    decision_tree_model = pickle.load(decision_tree_model_pkl)
    return decision_tree_model