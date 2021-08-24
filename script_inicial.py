#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import psycopg2 as pg
import os
import boto3
import csv
import requests
import time
import json


# In[ ]:


token = os.environ['MEMORY_TOKEN']
url = 'https://api.mypurecloud.com/api/v2/analytics/conversations/details/query'
login = 'https://login.mypurecloud.com/oauth/token?grant_type=client_credentials'
base_url = 'mypurecloud.com'


# In[ ]:


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
        return json.loads(token_auth.text)['access_token']
    return None


# In[ ]:


headers = {'Content-Type': "application/json", 
           'Accept': "application/json",
           'Authorization': f"{token_credentials['token_type']} {token_credentials['access_token']}"}


# In[ ]:


data = {"interval": f"2021-07-01T04:00:00.000Z/2021-07-15T04:00:00.000Z",
            "order": "asc",  
            "orderBy": "conversationStart",  
            "paging": {
                "pageSize": 100,
                "pageNumber": 1 
                }
           }


# In[ ]:


x = requests.post(url, data=json.dumps(data), headers=headers)
data_frame.append(pd.DataFrame.from_dict(x.json()['conversations']))
data = pd.concat(data_frame)
info = []


# In[ ]:


for index, row in data.iterrows():
    info_row = {}
    info_row['conversationEnd'] = row['conversationEnd']
    info_row['conversationId'] = row['conversationId']
    info_row['conversationStart'] = row['conversationStart']
    info_row['originatingDirection'] = row['originatingDirection']
    info_row['dnis'] = None
    info_row['ani'] = None
    info_row['contact_id'] = None
    info_row['contact_list_id'] = None
    info_row['campaing_id'] = None
    info_row['result'] = None
    for participant in row['participants']:
        for i in participant['sessions']:
            if participant['purpose'] == 'customer':
                try:
                    info_row['campaing_id'] = i['outboundCampaignId']
                    info_row['contact_list_id'] = i['outboundContactListId']
                    info_row['contact_id'] = i['outboundContactId']
                    info_row['dnis'] = i['dnis']
                    info_row['ani'] = i['ani']
                except:
                    pass
            elif participant['purpose'] == 'ivr':
                try:
                    info_row['dnis'] = i['sessionDnis']
                    info_row['ani'] = i['ani']
                except:
                    pass
            elif participant['purpose'] == 'outbound':
                for j in i['segments']:
                    if 'wrapUpCode' in j:
                        info_row['result'] = j['wrapUpCode']
    info.append(info_row)

