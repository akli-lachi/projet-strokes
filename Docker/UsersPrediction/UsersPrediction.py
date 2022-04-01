import os
import requests
from requests.auth import HTTPBasicAuth

# dÃ©finition de l'adresse de l'API
api_address = 'my_sp_from_compose'
# port de l'API
api_port = 8000

# requÃªte
r = requests.post(
    url='http://{address}:{port}/users/prediction'.format(address=api_address, port=api_port), auth=HTTPBasicAuth('alice', 'wonderland'),
    params= {
        'model': 'rf'
    },
    json=[
        {
        "gender": 0,
        "age": 20,
        "hypertension": 0,
        "heart_disease": 0,
        "ever_married": 0,
        "urban_residence": 0,
        "avg_glucose_level": 100,
        "bmi": 20,
        "smoking_status": 0
        },
        {
        "gender": 0,
        "age": 80,
        "hypertension": 1,
        "heart_disease": 1,
        "ever_married": 0,
        "urban_residence": 0,
        "avg_glucose_level": 300,
        "bmi": 60,
        "smoking_status": 1
        }
    ]

)

output = '''
============================
    Users prediction test
============================

request done at "/users/prediction"
| model="rf"

expected result = [0,1]
actual result = {result}

==>  {test_status}

'''

# statut de la requête
status_code = r.status_code
# resultat de la requête
result = r.json()

# affichage des rÃ©sultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(result=result, test_status=test_status))

log=os.environ.get('LOG')

# impression dans un fichier
if int(log) == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)

