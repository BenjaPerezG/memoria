# import numpy as np
# import psycopg2 as pg
# import boto3
# import csv
# import time

import os
import pandas as pd
import requests
import json

token = os.environ['MEMORY_TOKEN']
url = 'https://api.mypurecloud.com/api/v2/analytics/conversations/details/query'
login = 'https://login.mypurecloud.com/oauth/token?grant_type=client_credentials'
base_url = 'mypurecloud.com'


def auth(token, base_url):
    token_auth = requests.post(
        f'https://login.{base_url}/oauth/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {token}'
        },
        data={
            'grant_type': 'client_credentials'
        }
    )
    if token_auth.status_code == 200:
        return json.loads(token_auth.text)
    return None


token_credentials = auth(token, base_url)


headers = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Authorization': f"{token_credentials['token_type']} {token_credentials['access_token']}"}


query_structure = {
    "interval": "2021-07-01T04:00:00.000Z/2021-07-07T04:00:00.000Z",
    "order": "asc",
    "orderBy": "conversationStart",
    "paging": {
        "pageSize": 100,
        "pageNumber": 1
        }
}

data = []
filtered_data = {}
flows = []

answer = requests.post(url, data=json.dumps(query_structure), headers=headers)

for conversation in answer.json()['conversations']:
    if conversation['originatingDirection'] == 'inbound':
        for participant in conversation['participants']:
            for session in participant['sessions']:
                if 'flow' in session.keys():
                    filtered_data[conversation['conversationId']] = {
                        'flow' : session['flow']['flowId'],
                        'participant' : participant['participantId'],
                    }
                    flows.append(session['flow'])
        data.append(conversation)

outcomes = []

for flow in flows:
    if 'outcomes' in flow.keys():
        outcomes.append(flow.pop('outcomes'))

outcomes_frame = pd.DataFrame.from_dict(outcomes)
data_frame = pd.DataFrame.from_dict(filtered_data)
flow_frame = pd.DataFrame.from_dict(flows)

outcomes_frame.to_csv('outcomes.csv')
data_frame.to_csv('out.csv')
flow_frame.to_csv('flows.csv')

"""for header in answer['conversations'][0]:
    print(header)"""
