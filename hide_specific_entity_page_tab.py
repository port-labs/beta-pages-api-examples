import os
import requests

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
API_URL = os.environ.get('API_URL')

BLUEPRINT_IDENTIFIER = 'Node'
PAGE_IDENTIFIER = f"{BLUEPRINT_IDENTIFIER}Entity"

# to find your TAB_TO_HIDE_IDENTIFIER take a look of the output of the current_page variable with the following line inside the blueprintConfig key
# print(current_page['page']['widgets'][0]['groups'][0]['widgets'][1]['groups'][0]['widgets'][0])
TAB_TO_HIDE_IDENTIFIER = 'Cluster$upstream'

credentials = {'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
token_response = requests.post(f'{API_URL}/auth/access_token', json=credentials)

access_token = token_response.json()['accessToken']

# We will first get the page in order to make the update consistent
current_page = requests.get(f'{API_URL}/pages/{PAGE_IDENTIFIER}', headers = {'Authorization': f'Bearer {access_token}'}).json()['page']

# Hide tab in specific entity page related entities table
current_page['widgets'][0]['groups'][0]['widgets'][1]['groups'][0]['widgets'][0]['blueprintConfig'][TAB_TO_HIDE_IDENTIFIER]['hidden'] = True
response = requests.put(f'{API_URL}/pages/{PAGE_IDENTIFIER}', json=current_page, headers = {'Authorization': f'Bearer {access_token}'})

if response.status_code == 200:
    print('Page updated successfully')
else:
    print('Error updating page')

