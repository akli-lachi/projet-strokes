import os
import requests
from requests.auth import HTTPBasicAuth

# définition de l'adresse de l'API
api_address = '54.217.61.174'
# port de l'API
api_port = 8000

files = {'upload_file': open('strokestest.csv','rb')}

# requête
r = requests.post(
    url='http://{address}:{port}/file/prediction'.format(address=api_address, port=api_port), auth=HTTPBasicAuth('alice', 'wonderland'),
    params= {
        'model': 'rf'
    },
    files=files
)

output = '''
============================
    File prediction test
============================

request done at "/file/prediction"
| model="rf"

expected result = [1,1,1,1......,0,0,0,0,0]
actual result = {status_code}

==>  {test_status}

'''

# statut de la requête
status_code = r.status_code
# resultat de la requête
result = r.json()

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))

log=os.environ.get('LOG')

# impression dans un fichier
if int(log) == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)
