import json

from helpers import load_config, create_logger
from users import Users
from pre_processing import pre_processing
from modelisation import load_decision_tree_model, model_performance

conf = load_config()
logger = create_logger(conf)

# Test authentifcation
# users = Users(conf, logger)
# print(users.get_user_info('admin'))
# print(users.verify_username_password('admin', '4dm1N'))

# ALL_FEATURES = [
#     'age', 'avg_glucose_level', 'bmi', 'gender',  'ever_married', 'work_type', 
#     'residence_type', 'smoking_status', 'hypertension', 'heart_disease'
# ]

# QUANTITATIVE_FEATURES = ['age', 'avg_glucose_level', 'bmi']

# QUALITATIVE_FEATURES = [
#     'gender', 'ever_married', 'work_type', 'residence_type', 
#     'smoking_status', 'hypertension', 'heart_disease'
# ]


X_train, X_test, y_train, y_test = pre_processing(conf, sampling=False)    

model = load_decision_tree_model(conf)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

perf = model_performance(conf, y_test, y_pred)
print(json.dumps(perf))


