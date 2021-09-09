import base64, requests, sys, os, json

print("---------------------------------------------------")
print("- Genesys Cloud Python Client Credentials Example -")
print("---------------------------------------------------")

# CLIENT_ID = os.environ['GENESYS_CLOUD_CLIENT_ID']
# CLIENT_SECRET = os.environ['GENESYS_CLOUD_CLIENT_SECRET']
ENVIRONMENT = 'mypurecloud.com'  # eg. mypurecloud.com
authorization = os.environ['MEMORY_TOKEN']


# Base64 encode the client ID and client secret
# authorization = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "ISO-8859-1")).decode("ascii")

# Prepare for POST /oauth/token request
request_headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
request_body = {
    "grant_type": "client_credentials"
}

# Get token
response = requests.post(f"https://login.{ENVIRONMENT}/oauth/token", data=request_body, headers=request_headers)

# Check response
if response.status_code == 200:
    print("Got token")
else:
    print(f"Failure: { str(response.status_code) } - { response.reason }")
    sys.exit(response.status_code)

# Get JSON response body
response_json = response.json()

# Prepare for GET /api/v2/authorization/roles request
requestHeaders = {
    "Authorization": f"{ response_json['token_type'] } { response_json['access_token']}"
}
headers = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Authorization': f"{response_json['token_type']} {response_json['access_token']}"}

# Get roles
api_url = '/api/v2/authorization/roles'
api_url1 = '/api/v2/analytics/flows/observations/query'

request = {
    'filter': {
        'type': 'any',
        'clauses': [
            {
                'type': '',
                'dimensions': '',
                'operator': '',
                'value': '',
                'range': {
                    'gte': 0,
                }
            }
        ],
        'predicates': [
            ''
        ]
    },
    'metrics': [
        "yes"
    ],
}

# response = requests.get(f"https://api.{ENVIRONMENT}{api_url}", headers=requestHeaders)
response = requests.post(f"https://api.{ENVIRONMENT}{api_url1}", data=json.dumps(request), headers=headers)

# Check response
if response.status_code == 200:
    print("Got roles")
else:
    print(f"Failure: { str(response.status_code) } - { response.reason }")
    sys.exit(response.status_code)

# Print headers
print('\nHeaders:')
for header in response.json():
    print(f' {header}')

# Print roles
print("\nRoles:")
for entity_header in response.json()["entities"][0]:
    print(f"  { entity_header }")

print("\nDone")
