# -*- coding: utf-8 -*-
import pandas as pd

from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split


ALL_FEATURES = ['age', 'avg_glucose_level', 'bmi', 'gender', 
                'ever_married', 'work_type', 'residence_type', 
                'smoking_status', 'hypertension', 'heart_disease']

QUANTITATIVE_FEATURES = ['age', 'avg_glucose_level', 'bmi']

QUALITATIVE_FEATURES = ['gender', 'ever_married', 'work_type', 
                        'residence_type', 'smoking_status', 'hypertension',
                        'heart_disease']

TARGET = ['stroke']


def load(conf):
    file = conf['data.path'] + '/' + conf['data.file']

    if conf['data.file.header'] == 'true':
        header = 1
    else:
        header = 0
    
    data = pd.read_csv(file, sep=conf['data.file.separator'], header=0)
    df = data.copy()
    df = df.rename(columns={"Residence_type": "residence_type"})
    df = df.drop(['id'], axis=1)
    return(df)

def encoding(df, qualitative_features):
    gender_code = {'Other': 0,
                   'Male': 1,
                   'Female': 2}
        
    ever_married_code = {'No': 0,
                         'Yes': 1}
    
    work_type_code = {'Private': 0,
                      'Self-employed': 1,
                      'children': 2,
                      'Govt_job': 3,
                      'Never_worked': 4}
    
    residence_type_code = {'Urban': 0,
                           'Rural': 1}
        
    smoking_status_code = {'never smoked': 0,
                           'Unknown': 1,
                           'formerly smoked': 2,
                           'smokes': 3}
    
    df.loc[:, 'gender'] = df['gender'].map(gender_code)
    df.loc[:, 'ever_married'] = df['ever_married'].map(ever_married_code)
    df.loc[:, 'work_type'] = df['work_type'].map(work_type_code)

    df.loc[:, 'residence_type'] = \
        df['residence_type'].map(residence_type_code)
    
    df.loc[:, 'smoking_status'] = \
        df['smoking_status'].map(smoking_status_code)
    
    return df.loc[:, qualitative_features]

def scaling(df, quantitative_features):
    scaler = RobustScaler()    
    return pd.DataFrame(data=scaler.fit_transform(df[quantitative_features]),
                        columns=quantitative_features)

def imputation(df):    
    df.bmi.fillna(df.bmi.mean(), inplace=True)    
    return df

def pre_processing(conf, sampling=False):    
    df = load(conf)
    
    # df = imputation(df)
    
    # df_quantitative = scaling(df, QUANTITATIVE_FEATURES)
    df_quantitative = df.loc[:, QUANTITATIVE_FEATURES]
    df_qualitative = encoding(df, QUALITATIVE_FEATURES)

    X = pd.concat([df_quantitative, df_qualitative], axis=1)
    y = df.loc[:, 'stroke']

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.2, random_state=0)

    # Sur-échantillonnage Target :
    # - Cela est fait seulement sur la partie train du dataset, effectivement,
    #   effectuer un resampling sur les données de test fausse les résultats
    # - Cloner les samples avant découpe train / test, va inévitablement 
    #   provoquer la présence de samples du test dans le train et donc un leak
    if sampling:        
        rOs = RandomOverSampler()
        X_train, y_train = rOs.fit_resample(X_train, y_train)

    return X_train, X_test, y_train, y_test