import os
import requests

from requests.auth import HTTPBasicAuth


def api_result(output,
               endpoint,
               username,
               password,
               expected_status_code,
               status_code):        
    
    if status_code == expected_status_code:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    print(output.format(endpoint=endpoint,
                        username=username,
                        password=password,
                        expected_status_code=expected_status_code,
                        status_code=status_code,
                        test_status=test_status))

    # Ecriture dans un fichier
    if os.environ.get('API_LOG') == '1':    
        log_folder = os.environ.get('API_LOG_PATH') + '/api_strokes_test.log'
        with open(log_folder, 'a') as file:        
            file.write(output.format(endpoint=endpoint,
                                     username=username,
                                     password=password,
                                     expected_status_code=expected_status_code,
                                     status_code=status_code,                                     
                                     test_status=test_status))


# définition de l'adresse de l'API
api_address = os.environ.get('API_HOST')
# api_address = '172.23.0.3'

# port de l'API
api_port = str(os.environ.get('API_PORT'))
# api_port = '8000'

############ API test authentication ############
api_endpoint = 'auth_test'
api_username = 'alice'
api_password = 'wonderland'

def get_output():
    output = '''
=====================================================
    Strokes API tests - Authentication
=====================================================
request done at "{endpoint}"
| username="{username}"
| password="{password}"

expected status result =  {expected_status_code}
actual status result = {status_code}
==> {test_status}
    '''
    return output

# Call API
r = requests.get(
    url='http://{address}:{port}/{endpoint}'.format(address=api_address,
                                                    port=api_port,
                                                    endpoint=api_endpoint),
    auth=HTTPBasicAuth('alice', 'wonderland')
)

# Display and write log API result
api_result(
    get_output(),
    api_endpoint,
    api_username,
    api_password,
    '200',
    str(r.status_code)
)


############ API test perf models ############
api_endpoint = 'model/perf'
api_username = 'alice'
api_password = 'wonderland'

# Call API - Decision Tree
r = requests.get(
    url='http://{address}:{port}/{endpoint}'.format(address=api_address,
                                                    port=api_port,
                                                    endpoint=api_endpoint),
    auth=HTTPBasicAuth('alice', 'wonderland'),
    params={'model_name': 'decision_tree'}
)

def get_output_tree():
    output = '''
=====================================================
    Strokes API tests - Perf Decision Tree
=====================================================
request done at "{endpoint}"
| username="{username}"
| password="{password}"

expected status result =  {expected_status_code}
actual status result = {status_code}
==> {test_status}
    '''
    return output

# Display and write log API result
api_result(
    get_output_tree(),
    api_endpoint,
    api_username,
    api_password,
    '200',
    str(r.status_code)
)


# Call API - Logistic Regression
r = requests.get(
    url='http://{address}:{port}/{endpoint}'.format(address=api_address,
                                                    port=api_port,
                                                    endpoint=api_endpoint),
    auth=HTTPBasicAuth('alice', 'wonderland'),
    params={'model_name': 'logistic_regression'}
)

def get_output_lr():
    output = '''
=====================================================
    Strokes API tests - Perf Logistic Regression
=====================================================
request done at "{endpoint}"
| username="{username}"
| password="{password}"

expected status result =  {expected_status_code}
actual status result = {status_code}
==> {test_status}
    '''
    return output

# Display and write log API result
api_result(
    get_output_lr(),
    api_endpoint,
    api_username,
    api_password,
    '200',
    str(r.status_code)
)


# Call API - KNeighbors
r = requests.get(
    url='http://{address}:{port}/{endpoint}'.format(address=api_address,
                                                    port=api_port,
                                                    endpoint=api_endpoint),
    auth=HTTPBasicAuth('alice', 'wonderland'),
    params={'model_name': 'kneighbors'}
)

def get_output_kn():
    output = '''
=====================================================
    Strokes API tests - Perf KNeighbors
=====================================================
request done at "{endpoint}"
| username="{username}"
| password="{password}"

expected status result =  {expected_status_code}
actual status result = {status_code}
==> {test_status}
    '''
    return output

# Display and write log API result
api_result(
    get_output_kn(),
    api_endpoint,
    api_username,
    api_password,
    '200',
    str(r.status_code)
)