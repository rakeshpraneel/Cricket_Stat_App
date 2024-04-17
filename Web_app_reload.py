import requests
import json

secret_file = '{file_name}'
secret_values = {}
with open(secret_file,'r') as sf:
    secret_values = json.loads(sf.read())
username = secret_values['USERNAME']
token = secret_values['SM_API_TOKEN']
host = secret_values['HOST']
domain_name = secret_values['DOMAIN_NAME']

print(f"User name: {username}")
print(f"token: {token}")
print(f"host: {host}")
print(f"domain name: {domain_name}")

response = requests.post(
    'https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        host=host, username=username, domain_name=domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('Web app Reloaded: ')
    print(response.content)
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
