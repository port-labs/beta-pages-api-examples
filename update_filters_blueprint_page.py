import os
import requests

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
API_URL = os.environ.get('API_URL')

BLUEPRINT_IDENTIFIER = 'Node'

# the page identifier will be the blueprint identifier in plural for example Node -> Nodes
PAGE_IDENTIFIER = f"Nodes"

credentials = {'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
token_response = requests.post(f'{API_URL}/auth/access_token', json=credentials)

access_token = token_response.json()['accessToken']

# We will first get the page in order to make the update consistent
current_page = requests.get(f'{API_URL}/pages/{PAGE_IDENTIFIER}', headers = {'Authorization': f'Bearer {access_token}'}).json()['page']

# Update the filters to look for all the entities with the identifier test
current_page['widgets'][0]['blueprintConfig'] = {
    f"{BLUEPRINT_IDENTIFIER}": {
        "filterSettings": {
            "filterBy": {
                "combinator": "and",
                "rules": [
                    {
                        "property": "$identifier",
                        "value": [
                            "test"
                        ],
                        "operator": "="
                    }
                ]
            }
        }                            
    }
}

response = requests.put(f'{API_URL}/pages/{PAGE_IDENTIFIER}', json=current_page, headers = {'Authorization': f'Bearer {access_token}'})

if response.status_code == 200:
    print('Page updated successfully')
else:
    print('Error updating page')

